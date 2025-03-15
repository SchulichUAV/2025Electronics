from time import sleep
import pigpio

pi = None

pin_dict = {
    1: 14, #pin1
    2: 15, #pin2
    3: 18, #pin3
    4: 23  #pin4
}

def set_servo_angle(pin, target_angle):
    """Gradually moves the servo to the target angle."""
    step = 15
    delay = 0.003
    current_pulse = max(pi.get_servo_pulsewidth(pin), 500)    
    current_angle = (current_pulse - 500) * (180 / 2000)
    
    if target_angle <= current_angle:
        step = -step

    #will increment the current angle to the target angle using step
    for angle in range(int(current_angle), target_angle + step, step):
        pulse_width = 500 + (angle / 180.0) * 2000
        pi.set_servo_pulsewidth(pin, pulse_width)
        sleep(delay)

def configure_servos():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        print("Failed to connect")
        exit()

def payload_release(payload_id):
    try:
        pin = pin_dict[payload_id]
        set_servo_angle(pin, 0)
        print(f"Successfully opened servo: {pin}")
        sleep(3)
        set_servo_angle(pin, 180)
        print(f"Closing servo: {pin}")
    except Exception as e:
        print(f"Could not open or close servo. Error: {e}")