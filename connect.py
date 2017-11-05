import sys
import time
#import experiment as exp
import experiment_AndrewTest as experiment
import experiment_AndrewTest as exp
import numpy as np
import Dynamics as dy
import arduino_serial
import os
import datetime

stream_data=exp.mocap()
save_file_name_cam=datetime.datetime.today().strftime('%Y%m%d-%H:%M:%S-deadbeat-v0.1.0-jump5_stair.csv');
#save_file_name_ard=datetime.datetime.today().strftime('%Y%m%d-%H:%M:%S-deadbeat-v0.1.0-arduino.csv');


getdata = []; time_cam = []; arduino = [];
#cmd('TakeControl')

try:
    stream_data.startRTMeasurement();
    timelength = 60;
    #getdata=stream_data.streamDataStore(timelength);
    #os.system('arduino_serial.py')
    #arduino, time1 = threading.Thread(target = arduino_serial.readArd(timelength)).start();
    #getdata, time = threading.Thread(target = stream_data.streamDataStoreRev(timelength)).start();
    getdata, time_cam,arduino = stream_data.streamDataStoreRev(timelength)
    print ('*****')
    print getdata
    #arduino = threading.Thread(target = arduino_serial.readArd(timelength)).start();
    #print getdata
    stream_data.stopRTMeasurement();
  
except Exception as ex:
  print 'EXCEPT:',ex


length_cam = int (np.shape(getdata)[0]);
length_ard = len(arduino);
#a = 0
X=[];
Y=[];
TIME_CAM=[];
#TIME_ARD=[];
ARDUINO = [];

#print getdata[1][('y')]

for i in range(length_cam):
   
   X.append(getdata[i][('y')])
   Y.append(getdata[i][('x')])
   TIME_CAM.append(time_cam[i])
   ARDUINO.append(arduino[i])

#for i in range(length_ard):
#   ARDUINO.append(arduino[i].astype(float))
#   TIME_ARD.append(time_ard[i])


#ARDUINO.append(arduino[i])
#######################################
   #if (len(getdata[i][('y')])==4):
         #X.append(getdata[i][('y')])
         #Y.append(getdata[i][('x')])
         #time_filterd.append(time[i])
    #    p1,p2,p3 = dy.arrange_points(getdata[2*i+1]);
    #    PO1.append(p1);
#	PO2.append(p2);
#	PO3.append(p3);
   #else :
        #pass
        #print ("bad data",a); 
        #a = a + 1;
#########################################


#print X



#save as csv

import pandas as pd
dataframe_cam = {'x': X, 'y': Y, 'time' : TIME_CAM, 'ard': ARDUINO}
df = pd.DataFrame(dataframe_cam, columns = ['x', 'y', 'time','ard'])
df.to_csv(save_file_name_cam)

#dataframe_cam = {'time' : TIME_ARD, 'ard': ARDUINO}
#df = pd.DataFrame(dataframe_cam, columns = ['time','ard'])
#df.to_csv(save_file_name_ard)

