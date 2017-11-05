'''
Script to figure out timing to start a measurement, stop measurement, and 
save measurement using qualisys RT.
Previously, when not streaming the data, the saved .qtm file would be empty.
(When streaming, I didn't check the .qtm file, may or may not have been empty
'''

from experiment import mocap
import time

mo = mocap()
for i in [1,2]:
  mo.startCapture()
  time.sleep(10)
  print '*'*20
  print 'Saving!!!'
  mo.stopCapture('Test')




