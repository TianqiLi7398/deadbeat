import random

c=random.randint(-9,9)
print c




import serial
ser= serial.Serial('/dev/ttyUSB0', 115200)
while 1:
    print ser.readline()


