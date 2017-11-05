import experiment
import numpy as np
import pickle as pkl
from datetime import datetime

ex = experiment.experiment()

jumpPos =2
landPos = 2
#for landPos in np.arange(.5,2.1,.1):
for landPos in np.arange(.5,0.8,.1):
#for landPos in [ .5]:
  print '\n'*2
  print '*'*10
  print 'landPos: '+str(landPos)
  experiment_data = ex.conduct_experiment(landPos,jumpPos,True)
  filename = 'rawdata/'+\
    datetime.now().strftime('%Y-%m-%d::%H:%M:%S_')+\
    str(landPos).replace('.','_')+'##'+str(jumpPos).replace('.','_')+'.pkl'
  experiment_data['jumpPos']=jumpPos
  experiment_data['landPos']=landPos
  
#  data = {'jumpPos':jumpPos,
#          'landPos':landPos,
#          'time':experiment_data['time'],
#          'frames':experiment_data['frames'],
#          't1':experiment_data['t1'],
#          't2':experiment_data['t2']}
#  with open(filename,'w') as fp:
#    pkl.dump(experiment_data,fp)
