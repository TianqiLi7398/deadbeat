import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
import random
import serial

tempF=[]
cnt=0

def makeFig(): #Create a function that makes our desired plot
    plt.ylim(0,9)                                 #Set y min and max values
    plt.title('My Live Streaming Sensor Data')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Temp F')                            #Set ylabels
    plt.plot(tempF, 'ro-', label='Degrees F')       #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend
    
ser= serial.Serial('/dev/ttyUSB0', 115200)
while 1:
    
    #c=ser.readline()
    #dataarray=c.split('/t')
    position=random.uniform(0,9)
    tempF.append(position)
    drawnow(makeFig)
    plt.pause(.001)
    cnt=cnt+1
    if (cnt>50):
        tempF.pop(0)
        #pressure.pop(0)



