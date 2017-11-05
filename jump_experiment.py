import serial
import sys
import time
import numpy as np
from socket import ( IPPROTO_TCP, TCP_NODELAY )

ip = '192.168.56.1'
baudrate = 115200 #set in the arduino code
port = '/dev/ttyS2'
experimentLength = 10 #in seconds

ysign = -1. # camera return (sub) pixel values, y axis pointed down

execfile('qualisys.py') 

def cmd( line, loop=True, delay=.05 ):
  # loop - retrieve all sent tcp packets
  time.sleep(delay)
  cmd = line.strip()
  print cmd
  cmds.append(cmd)
  sesh.append(cmd)
  qtm.command(cmd)
  time.sleep(delay)
  if loop:
    do_tcp_loop()

def do_tcp_loop():
  pkt = 1
  while pkt:
    pkt = qtm.ptcp.next()
    print 'TCP pkt =',pkt
    pkts.append(('TCP',pkt))
    sesh.append(('TCP',pkt))

def dataIntoArrays(experimentLength):
  # experimentLength is time of experiment in seconds
  # data time is from the packet time
  pkt = 1
  data = []
  startTime = time.time()
  #while pkt:
  print 'here'
  if experimentLength == None:
    whileCondition = lambda: pkt
  else:
    whileCondition = lambda: time.time()-startTime<experimentLength
  #while time.time()-startTime < experimentLength:
  while whileCondition():
    pkt = qtm.ptcp.next()
    if not isinstance(pkt,DataPacket):
      continue
    pkt_time = pkt.time[0]
    if pkt_time == 0: #packet has no data
      continue
    frame = pkt.frame[0]
    pkt_data = pkt.comp[0].cam[0] #not sure why comp index is 0, cam[0] as we only have one camera for now
    # maybe a pandas table here?
    data.append({'time':pkt_time, 'frame':frame, 'data':pkt_data})
  return data
    

cmds = []
pkts = []
sesh = []

ser = serial.Serial()
ser.baudrate = baudrate
ser.port = port

qtm = QTM()
qtm.tcp.setsockopt(IPPROTO_TCP,TCP_NODELAY,1)
qtm.connect(ip)

if not qtm.isConnected():
  print 'failed to connect'
  sys.exit(0)
cmd('TakeControl')
cmd('Version 1.9')
#cmd('Load TestSave')
#cmd('Start RTFromFile',delay=1.)
cmd('New',delay=1.) #takes a bit to start new connection
cmd('Start', delay=1.)
#time.sleep(experimentLength)
#cmd('StreamFrames AllFrames UDP:%d 2D' % 
#      (qtm.udp.getsockname()[1]))
cmd('StreamFrames AllFrames 2D', loop = False)
data = dataIntoArrays(experimentLength)
#data = dataIntoArrays(None)
cmd('StreamFrames Stop',loop=False)
cmd('Save TestMeasurement')
#cmd('Stop')
cmd('ReleaseControl')

times = []
frames = []
track1 = []
track2 = []
data_len = []
for dat in data:
  #hard coding to assume only two tracks for now
  times.append(dat['time'])
  frames.append(dat['frame'])
  
  data_len.append(len(dat['data']))
  #kludgy
  if len(dat['data'])>0:
    x1 = dat['data'][0][0]
    y1 = ysign * dat['data'][0][1]
  else:
    x1 = np.NaN
    y1 = np.NaN
  if len(dat['data'])>1:
    x2 = dat['data'][1][0]
    y2 = ysign * dat['data'][1][1]
  else:
    x2 = np.NaN
    y2 = np.NaN
  track1.append( np.array([x1,y1]) )
  track2.append( np.array([x2,y2]) )

track1 = np.vstack(track1)
track2 = np.vstack(track2)
fd = np.diff(frames)
td = np.diff(times)

