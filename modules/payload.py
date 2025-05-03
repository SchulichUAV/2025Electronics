from time import sleep
from adafruit_servokit import ServoKit


def payload_release(kit, servo_num):
    try:
        kit.servo[servo_num].angle = 10
        print(f"Successfully opened servo: {kit.servo[servo_num]}")
        sleep(3)
        kit.servo[servo_num].angle = 180
        print(f"Closing servo: {kit.servo[servo_num]}")
    except Exception as e:
        print(f"Could not open or close servo. Error: {e}")

def set_servo_state(servo, open):
    if open:
        print(f"Opening servo{servo}. Not automatically closing.")
        servo.angle = 180
    else:
        print(f"Closing servo{servo}.")
        servo.angle = 10