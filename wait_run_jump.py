'''
Go through a sequence of jump/land positions waiting for 
user to hit enter before proceeding
(Because qualisys sucks)
'''

import numpy as np
from experiment import hopper

hop = hopper()
hop.openSer()

jumpPos = 2
landPos = 2
#for landPos in np.arange(0.5, 1.1, .1):
for landPos in [0.5]:
  raw_input("Press enter to continue...")
  print "land Pos: "+str(landPos)
  hop.jump(landPos,jumpPos)

hop.closeSer()

