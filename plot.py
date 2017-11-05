import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
import random
import serial

tempF=[]
cnt=0

def makeFig(): #Create a function that makes our desired plot
    plt.ylim(0,5)                                 #Set y min and max values
    plt.title('My Live Streaming Sensor Data')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Temp F')                            #Set ylabels
    plt.plot(tempF, 'ro-', label='Degrees F')       #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend
    
ser= serial.Serial('/dev/ttyUSB0', 115200)
while 1:
    if (ser.inWaiting()==1):
       pass
    c=ser.readline()
    ser.read_all()
    #print c
    dataarray=c.split(',')
    position=float(dataarray[0])
    print position       # from here we can get updating data
    tempF.append(position)
    drawnow(makeFig)
    plt.pause(.00001)
    cnt=cnt+1
    if (cnt>500):
        tempF.pop(0)
        #pressure.pop(0)



