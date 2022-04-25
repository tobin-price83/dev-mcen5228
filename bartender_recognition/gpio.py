import Jetson.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
sensor = 7;
GPIO.setup(sensor, GPIO.OUT)

if GPIO.input(sensor) == True:
    print("Detection!")
else:
    print("Nothing Is There")