import numpy as np
import experiment

mocap = experiment.mocap()

mocap.startRTMeasurement()
data = mocap.streamDataStore(10)
mocap.stopRTMeasurement(None)

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
  ysign = -1
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

print np.max(fd)
