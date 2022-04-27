import Jetson.GPIO as GPIO

def cup_close():
    if GPIO.input(7) == 0:
        return True
    else:
        return False

GPIO.setmode(GPIO.BOARD)
sensor = 7
GPIO.setup(sensor, GPIO.IN)
print(cup_close())
