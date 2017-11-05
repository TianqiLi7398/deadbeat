import time
import serial
import numpy as np;

def readArd(length):
    Ard=serial.Serial('/dev/ttyUSB0',115200)
    start_time = time.time()
    mydata=[]; Time = [];
    num = 0
    while (time.time() - start_time<length):
    #try:
        if (Ard.inWaiting()>0):
            print Ard.readline()
            Time.append(time.time())
            mydata.append(Ard.readline());
            num=num+1;
            print num
    #except (KeyboardInterrupt, SystemExit):
            #raise
    #except:
        #break
    return mydata, Time
