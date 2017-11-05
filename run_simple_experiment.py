'''
save the data on the qualisys side, no streaming
'''
import experiment
import numpy as np

ex = experiment.experiment()
ex.experimentLength = 15

jumpPos =2
landPos = 2
for landPos in np.arange(.5,2.1,.1):
#for landPos in np.arange(.5,0.7,.1):
#for landPos in [ .5]:
  print '\n'*2
  print '*'*10
  print 'landPos: '+str(landPos)
  ex.conduct_experiment_nostream(landPos,jumpPos)
