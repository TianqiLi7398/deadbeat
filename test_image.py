

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

if not qtm.isConnected():
  print 'failed to connect'
  sys.exit(0)

cmd('Version 1.13')
cmd('TakeControl')

try:
  cmd('New')
  time.sleep(2)

  cmd('Start')
  time.sleep(1)

  cmd('GetParameters')
  params = sesh[-2]

  cmd('GetCurrentFrame Image')
  image = sesh[-2]

  #cmd('Stop')
  #cmd('Close')
  #cmd('ReleaseControl')

except Exception as ex:
  print 'EXCEPT:',ex
  cmd('Stop')
  cmd('Close')
  cmd('ReleaseControl')
