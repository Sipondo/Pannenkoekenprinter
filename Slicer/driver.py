import atexit
import math
import threading
from time import sleep

import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT

mh = Adafruit_MotorHAT(addr=0x70)
pos_x = 0
pos_y = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setup([7], GPIO.OUT)


def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


def calibrate(myStepper):
    myStepper.setSpeed(20)
    calibration_length = 0;
    while (True):
        print("Length: " + str(calibration_length))
        if (raw_input("Continue?") == "N"):
            break;
        calibration_length = calibration_length + 200
        myStepper.step(200, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)

    while (True):
        print("Length: " + str(calibration_length))
        if (raw_input("Continue?") == "N"):
            break;
        calibration_length = calibration_length + 20
        myStepper.step(20, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)

    print("Final calibrated length: " + str(calibration_length))
    return calibration_length


atexit.register(turnOffMotors)

myStepper1 = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1                 # 30 RPM
myStepper2 = mh.getStepper(200, 2)  # 200 steps/rev, motor port #1            # 30 RPM
pos_x = 0
pos_y = 0

def stepper_worker(myStepper, distance, speed):
    myStepper.setSpeed(int(speed))
    if (distance > 0):
        myStepper.step(distance, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
    else:
        if (distance < 0):
            myStepper.step(abs(distance), Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)


def move(x, y):
    x = int(x/1)
    y = int(y/-1)
    # max_distance = math.sqrt(1.0 * x * x + y * y)
    x = x - pos_x
    y = y - pos_y
    pos_x = pos_x + x;
    pos_y = pos_y + y;

    # if (x != 0):
    #    st1 = threading.Thread(target=stepper_worker, args=(myStepper1, x, max(0, 30.0 * (abs(x)/max_distance))))
    # if (y != 0):
    #    st2 = threading.Thread(target=stepper_worker, args=(myStepper2, y, max(0, -3.0 + 24.0 * (abs(y)/max_distance))))

    if (x != 0):
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, x, 20))
    if (y != 0):
        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, y, 20))

    if (x != 0):
        st1.start()
    if (y != 0):
        st2.start()

    if (x != 0):
        st1.join()
    if (y != 0):
        st2.join()

#used_set = instruction_dictionary['kill_me']

def move_vector(vector):
    GPIO.cleanup(7)
    sleep(.2)
    for next_instruction in vector:
        move(next_instruction[0], next_instruction[1])
    print("beslag uit!")
    GPIO.cleanup(7)
    sleep(.2)
    pass

def print_vector(vector):
    GPIO.cleanup(7)
    sleep(.2)
    init_pos = vector[0]
    move(init_pos[0], init_pos[1])
    sleep(.2)
    print("beslag aan!")
    GPIO.setup([7], GPIO.OUT)
    GPIO.output(7, 1)
    sleep(.2)
    for next_instruction in vector[1:]:
        move(next_instruction[0], next_instruction[1])
    print("beslag uit!")
    GPIO.cleanup(7)
    sleep(.2)
