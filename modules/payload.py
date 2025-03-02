from gpiozero import AngularServo
from time import sleep

pin1 = 14 # Corresponds to bay 1
pin2 = 15 # Corresponds to bay 2
pin3 = 18 # Corresponds to bay 3
pin4 = 23 # Corresponds to bay 4

def configure_servos():
    servo1 = AngularServo(pin1, min_angle=0, max_angle=180,
    min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

    servo2 = AngularServo(pin2, min_angle=0, max_angle=180,
    min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

    servo3 = AngularServo(pin3, min_angle=0, max_angle=180,
    min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

    servo4 = AngularServo(pin4, min_angle=0, max_angle=180,
    min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

    return servo1, servo2, servo3, servo4

def payload_release(servo):
    try:
        servo.angle = 10
        print(f"Successfully opened servo: {servo}")
        sleep(3)
        servo.angle = 180
        print(f"Closing servo: {servo}")
    except Exception as e:
        print(f"Could not open or close servo. Error: {e}")

def set_servo_state(servo, open):
    if open:
        print(f"Opening servo{servo}. Not automatically closing.")
        servo.angle = 180
    else:
        print(f"Closing servo{servo}.")
        servo.angle = 10
