

import sys
import time

execfile('qualisys.py')

def cmd( line, delay=.05 ):
  time.sleep(delay)
  cmd = line.strip()
  print cmd
  cmds.append(cmd)
  sesh.append(cmd)
  qtm.command(cmd)
  time.sleep(delay)
  do_tcp('')

def do_tcp( line ):
  pkt = 1
  while pkt:
    pkt = qtm.ptcp.next()
    print 'TCP pkt =',pkt
    pkts.append(('TCP',pkt))
    sesh.append(('TCP',pkt))

ip = '192.168.56.1'
cmds = []
pkts = []
sesh = []

qtm = QTM()
qtm.connect(ip)
#print qtm.udp.getsockname()

if not qtm.isConnected():
  print 'failed to connect'
  sys.exit(0)

cmd('Version 1.15')

cmd('TakeControl')

try:
  cmd('Load _')

  cmd('Start RTFromFile')

  cmd('GetParameters')
  params = sesh[-2]

  #cmd('GetCurrentFrame 2D')
  #data = sesh[-2]


  #cmd('StreamFrames AllFrames UDP:%d 2D' % 
  #    (qtm.udp.getsockname()[1]))
  cmd('StreamFrames AllFrames 2D')

  for k in range(5):
    #pkt = qtm.pudp.next()
    #print 'UDP pkt =',pkt
    #pkts.append(('UDP',pkt))
    pkt = qtm.ptcp.next()
    print 'TCP pkt =',pkt
    pkts.append(('TCP',pkt))

  cmd('Stop')

  cmd('ReleaseControl')

except Exception as ex:
  print 'EXCEPT:',ex
  cmd('Stop')
  cmd('ReleaseControl')
