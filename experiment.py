import serial
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import qualisys
from socket import ( IPPROTO_TCP, TCP_NODELAY )
from datetime import datetime
import matplotlib
import serial

class mocap(object):
  ip = '192.168.56.1'
  def __init__(self):
    #execfile('qualisys.py') #a better way perhaps?
    self._cmds = []
    self._pkts = []
    self._sesh = []
    self._qtm = qualisys.QTM()
    self._qtm.tcp.setsockopt(IPPROTO_TCP,TCP_NODELAY,1)
    self._qtm.connect(mocap.ip)
    
    if not self._qtm.isConnected():
      print 'failed to connect'
      sys.exit(0)

  def cmd(self,  line, loop=True, delay=.05 ):
    # loop - if true, retrieve all sent tcp packets
    time.sleep(delay)
    cmd = line.strip()
    print cmd
    self._cmds.append(cmd)
    self._sesh.append(cmd)
    self._qtm.command(cmd)
    time.sleep(delay)
    if loop:
      self.do_tcp_loop()
  
  def do_tcp_loop(self):
    pkt = 1
    while pkt:
      pkt = self._qtm.ptcp.next()
      print 'TCP pkt =',pkt
      self._pkts.append(('TCP',pkt))
      self._sesh.append(('TCP',pkt))

  def getParameters(self):
    self.cmd('GetParameters All')
    for i in range(5,0,-1):
      if type(self._sesh[-i][1]) is qualisys.XML_Packet:
        break
    else:
      print 'XML Packet not recieved'
      return None
    xml = self._sesh[-i][1].root
    return xml 

  def streamDataStore(self, captureLength):
    # captureLength is time of experiment in seconds
    # data time is from the packet time
    pkt = 1
    data = []
    startTime = time.time()
    if captureLength == None:
      whileCondition = lambda: pkt
    else:
      whileCondition = lambda: time.time()-startTime<captureLength
    while whileCondition():
      pkt = self._qtm.ptcp.next()
      if not isinstance(pkt,qualisys.DataPacket):
        continue
      pkt_time = pkt.time[0]
      if pkt_time == 0: #packet has no data
        continue
      frame = pkt.frame[0]
      pkt_data = pkt.comp[0].cam[0] #not sure why comp index is 0, cam[0] as we only have one camera for now
      # maybe a pandas table here?
      data.append({'time':pkt_time, 'frame':frame, 'data':pkt_data})
      print pkt_data##########
    return data
  
  def streamDataStoreRev(self, captureLength):
       # captureLength is time of experiment in seconds
       # data time is from the packet time
     pkt = 1
     data = [];Time_Cam = [];#Arduino = []; Time_Ard = [];
     #Ard=serial.Serial('/dev/ttyUSB0',115200);
     #time.sleep(1);
     startTime = time.time();
     
     if captureLength == None:
       whileCondition = lambda: pkt
     else:
       whileCondition = lambda: time.time()-startTime<captureLength
     while whileCondition():
       pkt = self._qtm.ptcp.next();
       #print 2;
       if not isinstance(pkt,qualisys.DataPacket):
         continue
       pkt_time = pkt.time[0]
       if pkt_time == 0: #packet has no data
         continue
       frame = pkt.frame[0]
       pkt_data = pkt.comp[0].cam[0] #not sure why comp index is 0, cam[0] as we only have one camera for now
      # maybe a pandas table here?
       #data=pkt_data[0];
       #if (Ard.inWaiting()>0):
	   #Arduino.append(Ard.read(Ard.inWaiting()));
           #Time_Ard.append(int(round(time.time()*1000)));
           #print 2
       #else:
           #Arduino.append(0);
           #Time_Ard.append(int(round(time.time()*1000)));
       data.append(pkt_data);
       #data1=pkt_data[1];
       #print pkt_data
       
       Time_Cam.append(int(round(time.time()*1000)));
       #data.append({'time':pkt_time, 'frame':frame, 'data':pkt_data})
     return data,Time_Cam#, Arduino, Time_Ard



  def startMeasurement(self):
    self.cmd('TakeControl')
    #self.cmd('Stop')
    self.cmd('Version 1.9')
    self.cmd('New',delay=1.) #takes a bit to start new connection
    self.cmd('Start', delay=1.)

  def startRTMeasurement(self):
    self.startMeasurement()
    self.cmd('StreamFrames AllFrames 2D', loop = False)

  def streamFrames(self):
    self.cmd('StreamFrames AllFrames 2D', loop = False)

  def stopRTMeasurement(self, filename=None):
    #self.cmd('StreamFrames Stop',loop=False)
    self.cmd('Stop',loop = False)
    time.sleep(30) 
    if filename is not None:
      cmd = 'Save '+filename
      self.cmd(cmd)
    #self.cmd('Stop')
    self.cmd('Close',loop = False)
    self.cmd('ReleaseControl',loop = False)
  
  def stopMeasurement(self):
    self.cmd('StreamFrames Stop',loop=False)
    self.cmd('Stop')
    self.cmd('ReleaseControl')

  def startReplay(self, filename=None):
    self.cmd('TakeControl')
    self.cmd('Version 1.9')
    if filename is not None:
      self.cmd('Load '+filename)
    self.cmd('Start RTFromFile', delay=1) #takes a bit to start new connection
    self.cmd('StreamFrames AllFrames 2D', loop = False)

  '''
  startCapture and stopCapture are used when streaming the data
  is not needed
  '''
  def startCapture(self):
    self.cmd('TakeControl')
    self.cmd('Version 1.9')
    self.cmd('New', delay=5.) #give plenty of time to setup new measurement
    self.cmd('Start', delay=1.)

  def stopCapture(self, filename):
    self.cmd('Save '+filename)
    self.cmd('Close')
    self.cmd('ReleaseControl')
    time.sleep(1)


class hopper(object):
  baudrate = 115200 #set in the arduino code
  port = '/dev/ttyS2'

  def __init__(self):
    self._ser = serial.Serial()
    self._ser.baudrate = hopper.baudrate
    self._ser.port = hopper.port

  def openSer(self):
    self._ser.open()
  def closeSer(self):
    self._ser.close()
  
  def jump(self,landPosition, jumpPosition):
    #land position: motor angles when landing after jump
    #jump position: motor angles to jump to [0.5, 2] 
    # initial position before jump is 0.5
    cmd = "2; "+str(landPosition)+"; "+str(jumpPosition)+";"
    self._ser.write(cmd)
  

#maybe make these helper functions classmethods? staticmethods? another module?
def unwrap_data(data):
  '''
  When replaying data after it is recorded, data[0] is not 
  necessarily the first frame and the data is replayed
  Return data where data[0] corresponds to frame 1 (or lowest frame number),
        data[n] frame n+1 and the data is not repeated
  '''
  initial_frame = data[0]['frame']
  first_frame = None 
  for ind, dat in enumerate(data):
    if dat['frame']<initial_frame and not first_frame:
      first_frame = ind
    if dat['frame'] == initial_frame and first_frame and first_frame!=ind:
      break #found lowest frame number and data is repeating

  return (data*2)[first_frame:first_frame+(ind+2)] #unwrap the data, +2 including first

def process_data(data):
  ysign = -1. # camera return (sub) pixel values, y axis pointed down
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
      x1 = dat['data'][0][1]
      y1 = ysign * dat['data'][0][0]
    else:
      x1 = np.NaN
      y1 = np.NaN
    if len(dat['data'])>1:
      x2 = dat['data'][1][1]
      y2 = ysign * dat['data'][1][0]
    else:
      x2 = np.NaN
      y2 = np.NaN
    track1.append( np.array([x1,y1]) )
    track2.append( np.array([x2,y2]) )
  
  track1 = np.vstack(track1)
  track2 = np.vstack(track2)
  fd = np.diff(frames)
  if np.max(fd)>1:
    print '*'*20
    print 'Warning: missing frames!'
    print '*'*20

  return times, frames, track1, track2

class experiment(object):
  def __init__(self): 
    self.experimentLength = 10 #in seconds
    self.mocap = mocap()
    self.hopper = hopper()

 
  def conduct_experiment(self, landPos, jumpPos, saveData=True, streamAfter=False):
    '''
    StreamAfter - if streaming the data after collecting it
    '''
    if saveData:
      filename = datetime.now().strftime('%Y-%m-%d%%%%%H%%%M%%%S_')+\
	str(landPos).replace('.','_')+'__'+str(jumpPos).replace('.','_')
    else:
      filename = None

    self.hopper.openSer()
    #self.mocap.startRTMeasurement()
    self.mocap.startMeasurement()
    if not streamAfter:
      pass
      #self.mocap.streamFrames()
    self.hopper.jump(landPos, jumpPos) #there is a 1 second delay in the motion
    #data = self.mocap.streamDataStore( self.experimentLength)
    time.sleep(self.experimentLength)
    self.mocap.stopRTMeasurement(filename)
    #time.sleep(30)
    #if streamAfter:
    #  time.sleep(self.experimentLength)
    #  self.mocap.stopMeasurement()
    #else:
    #  self.mocap.stopRTMeasurement(filename)
    parameters = self.mocap.getParameters()
    self.hopper.closeSer()

    if streamAfter:
      data=unwrap_data(data)

    if 0:
      data_time, frames, t1, t2 = process_data(data)
      plt.figure()
      plt.plot(data_time, t1[:,1])
      plt.plot(data_time, t2[:,1])
      plt.ion()
      plt.show()
      experiment_data = {
        'time':data_time,
        'frames':frames,
        't1':t1,
         't2':t2,
         'parameters':parameters}
      return experiment_data
    return {}

  def conduct_experiment_nostream(self, landPos, jumpPos):
    '''
    '''
    filename = datetime.now().strftime('%Y-%m-%d##%H%%%M%%%S@')+\
	str(landPos).replace('.','_')+'&&'+str(jumpPos).replace('.','_')

    self.hopper.openSer()
    self.mocap.startCapture()
    self.hopper.jump(landPos, jumpPos) #there is a 1 second delay in the motion
    time.sleep(self.experimentLength)
    self.mocap.stopCapture(filename)
    self.hopper.closeSer()

