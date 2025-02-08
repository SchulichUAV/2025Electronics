from gpiozero import AngularServo
from time import sleep


servo1 = None
servo2 = None
servo3 = None
servo4 = None

def configure_servos():
    global servo1, servo2, servo3, servo4

    servo1 = AngularServo(14, min_angle=0, max_angle=180,
    min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

    servo2 = AngularServo(15, min_angle=0, max_angle=180,
    min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

    servo3 = AngularServo(18, min_angle=0, max_angle=180,
    min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

    servo4 = AngularServo(23, min_angle=0, max_angle=180,
    min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

def set_angles(angle1, angle2, angle3, angle4):
    global servo1, servo2, servo3, servo4

    servo1.angle = angle1
    servo2.angle = angle2
    servo3.angle = angle3
    servo4.angle = angle4

    print(f"Servo 1 angle: {angle1}\nServo 2 angle: {angle2}\nServo 3 angle: {angle3}\nServo 4 angle: {angle4}")

if __name__ == "__main__":
    try:
        angle1 = int(input("Enter angle for Servo 1 (0 to 180): "))
        angle2 = int(input("Enter angle for Servo 2 (0 to 180): "))
        angle3 = int(input("Enter angle for Servo 3 (0 to 180): "))
        angle4 = int(input("Enter angle for Servo 4 (0 to 180): "))
        set_angles(angle1, angle2, angle3, angle4)
    except KeyboardInterrupt:
        print("Program stopped by user")