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
        print "Length: " + str(calibration_length)
        if (raw_input("Continue?") == "N"):
            break;
        calibration_length = calibration_length + 200
        myStepper.step(200, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)

    while (True):
        print "Length: " + str(calibration_length)
        if (raw_input("Continue?") == "N"):
            break;
        calibration_length = calibration_length + 20
        myStepper.step(20, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)

    print "Final calibrated length: " + str(calibration_length)
    return calibration_length


atexit.register(turnOffMotors)

myStepper1 = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1                 # 30 RPM
myStepper2 = mh.getStepper(200, 2)  # 200 steps/rev, motor port #1            # 30 RPM


def stepper_worker(myStepper, distance, speed):
    myStepper.setSpeed(int(speed))
    if (distance > 0):
        myStepper.step(distance, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
    else:
        if (distance < 0):
            myStepper.step(abs(distance), Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)


def move(x, y):
    x = x/3
    y = y/-3
    global pos_x, pos_y
    max_distance = math.sqrt(1.0 * x * x + y * y)
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


instruction_dictionary = {
    'test': [
        ["MOVE", 500, 500],
        ["MOVE", -500, 500],
        ["MOVE", -500, -500],
        ["MOVE", 500, -500]
    ],
    'kill_me': [
        ["FLOW"],
        ["MOVE", -50, -50],
        ["MOVE", -50, -70],
        ["MOVE", -50, -90],
        ["MOVE", -40, -110],
        ["MOVE", -30, -130],
        ["MOVE", -20, -120],
        ["MOVE", 35, -90],#5
        ["MOVE", 80, 0],#4
        ["MOVE", 0, -80],#3
        ["MOVE", 80, -50],#2
        ["MOVE", 0, -50],#1
        ["MOVE", 30, 0],#middle
        ["MOVE", 0, -30],#middle
        ["MOVE", 60, 0],#middle offset
        ["MOVE", 0, 30],#middle
        ["MOVE", 30, 0],#middle
        ["MOVE", 0, 50],#1
        ["MOVE", 80, 50],#2
        ["MOVE", 0, 80],#3
        ["MOVE", 80, 0],#4
        ["MOVE", 35, 90],#5
        ["MOVE", -20, 120],
        ["MOVE", -30, 130],
        ["MOVE", -40, 110],
        ["MOVE", -50, 90],
        ["MOVE", -50, 70],
        ["MOVE", -50, 50],
        ["BLOCK"],
        ["MOVE", -35, -65], #offset 5
        ["FLOW"],
        ["MOVE", 0, -150],
        ["MOVE", -90, 0],
        ["BLOCK"],
        ["MOVE", -30, -80],
        ["FLOW"],
        ["MOVE", 120, 0],
        ["MOVE", 0, -90],
        ["BLOCK"],
        ["MOVE", 80, 0],
        ["FLOW"],
        ["MOVE", 0, 90],
        ["MOVE", 120, 0],
        ["BLOCK"],
        ["MOVE", -30, 80],
        ["FLOW"],
        ["MOVE", -90, 0],
        ["MOVE", 0, 150],
        ["BLOCK"],
        ["MOVE", 70, -600],
        ["FLOW"],
        ["MOVE", -220, 0],
        ["BLOCK"],
        ["MOVE", 0, -70],
        ["FLOW"],
        ["MOVE", 60, 0],
        ["MOVE", 0, 55],
        ["BLOCK"],
        ["MOVE", 10, -65],
        ["FLOW"],
        ["MOVE", 40, -40],
        ["BLOCK"],
        ["MOVE", -10, -10],
        ["FLOW"],
        ["MOVE", -20, 0],
        ["BLOCK"],
        ["MOVE", 60, 0],
        ["FLOW"],
        ["MOVE", -15, 0],
        ["BLOCK"],
        ["MOVE", 0, 25],
        ["FLOW"],
        ["MOVE", 25, 25],
        ["BLOCK"],
        ["MOVE", 10, 65],
        ["FLOW"],
        ["MOVE", 0, -55],
        ["MOVE", 60, 0],
        ["BLOCK"],
        ["MOVE", 80, 330],
        ["FLOW"],
        ["MOVE", -380, 0],
        ["BLOCK"],
        ["MOVE", 0, -20],
        ["FLOW"],
        ["MOVE", 130, -60],
        ["BLOCK"],
        ["MOVE", 60, 30],
        ["FLOW"],
        ["MOVE", 0, 30],
        ["BLOCK"],
        ["MOVE", 190, 0],
        ["FLOW"],
        ["MOVE", -130, -60],
        ["BLOCK"],
        ["MOVE", 150, -120],
        ["FLOW"],
        ["MOVE", -120, 0],
        ["MOVE", -30, 20],
        ["MOVE", 40, 30],
        ["MOVE", -60, 20],
        ["MOVE", -20, -60],
        ["MOVE", -20, -20],
        ["MOVE", -20, 20],
        ["MOVE", -20, 60],
        ["MOVE", -60, -20],
        ["MOVE", 40, -30],
        ["MOVE", -30, -20],
        ["MOVE", -120, 0],
        ["BLOCK"]#,
        #["MOVE", 210, 603]
    ],
    'square': [
        ["MOVE", -250, -950],
        ["FLOW"],
        ["MOVE", 500, 0],
        ["MOVE", 0, 500],
        ["MOVE", -500, 0],
        ["MOVE", 0, -450],
        ["BLOCK"],
        ["MOVE", 120, 70],
        ["FLOW"],
        ["MOVE", 260, 0],
        ["MOVE", 0, 260],
        ["MOVE", -260, 0],
        ["MOVE", 0, -260],
        ["MOVE", 130, 130],
        ["WAIT", 1],
        ["BLOCK"],
        ["MOVE", 0, 700]
    ],
    'heart': [
        ["MOVE", 0, -700],
        ["FLOW"],
        ["MOVE", -70, -100],
        ["MOVE", -70, -100],
        ["MOVE", -70, -100],
        ["MOVE", -70, -100],
        ["MOVE", 40, -70],
        ["MOVE", 40, 0],
        ["MOVE", 60, -10],
        ["MOVE", 40, 10],
        ["MOVE", 100, 100],
        ["MOVE", 100, -100],
        ["MOVE", 40, 0],
        ["MOVE", 60, -10],
        ["MOVE", 40, 10],
        ["MOVE", 40, 70],
        ["MOVE", -70, 100],
        ["MOVE", -70, 100],
        ["MOVE", -70, 100],
        ["MOVE", -40, 50],
        ["BLOCK"],
        ["MOVE", -30, -130],
        ["WAIT", 60],
        ["FLOW"],
        ["MOVE", -100, -250],
        ["BLOCK"],
        ["MOVE", 200, 0],
        ["FLOW"],
        ["MOVE", -100, 250],
        ["BLOCK"],
        ["MOVE", 0, 850]
    ],
    'star': [
        ["MOVE", 0, -500],
        ['FLOW'],
        ['MOVE', 20, -65],
        ['MOVE', 20, -65],
        ['BLOCK'],
        ['MOVE', 20, -65],
        ['FLOW'],
        ['MOVE', 77, -9],
        ['MOVE', 77, -9],
        ['BLOCK'],
        ['MOVE', 77, -9],
        ['FLOW'],
        ['MOVE', -58, -36],
        ['MOVE', -58, -36],
        ['BLOCK'],
        ['MOVE', -58, -36],
        ['FLOW'],
        ['MOVE', 10, -77],
        ['MOVE', 10, -77],
        ['BLOCK'],
        ['MOVE', 10, -77],
        ['FLOW'],
        ['MOVE', -49, 47],
        ['MOVE', -49, 47],
        ['BLOCK'],
        ['MOVE', -49, 47],
        ['FLOW'],
        ['MOVE', -49, -47],
        ['MOVE', -49, -47],
        ['BLOCK'],
        ['MOVE', -49, -47],
        ['FLOW'],
        ['MOVE', 10, 77],
        ['MOVE', 10, 77],
        ['BLOCK'],
        ['MOVE', 10, 77],
        ['FLOW'],
        ['MOVE', -58, 36],
        ['MOVE', -58, 36],
        ['BLOCK'],
        ['MOVE', -58, 36],
        ['FLOW'],
        ['MOVE', 77, 9],
        ['MOVE', 77, 9],
        ['BLOCK'],
        ['MOVE', 77, 9],
        ['FLOW'],
        ['MOVE', 20, 65],
        ['BLOCK'],
        ['MOVE', 18, 60],
        ['FLOW'],
        ['MOVE', 2, 5],
        ['BLOCK'],
        ['MOVE', 20, 65],
        ['MOVE', 0, -300],
        ["WAIT", 60],
        ['FLOW'],
        ['WAIT', 5],
        ['BLOCK'],
        ['MOVE', 0, 800],
    ],
    'flow': [
        ['FLOW'],
        ['WAIT', 60],
        ['BLOCK']
    ]
}

GPIO.cleanup(7)

used_set = instruction_dictionary['kill_me']

for next_instruction in used_set:

    if (next_instruction[0] == "MOVE"):
        move(next_instruction[1], next_instruction[2])
    elif (next_instruction[0] == "WAIT"):
        sleep(next_instruction[1])
        print "Sleeping for: " + str(next_instruction[1])
    elif (next_instruction[0] == "FLOW"):
        print "beslag aan!"
        GPIO.setup([7], GPIO.OUT)
        GPIO.output(7, 1)
        sleep(.2)
    elif (next_instruction[0] == "BLOCK"):
        print "beslag uit!"
        GPIO.cleanup(7)
        sleep(.2)

GPIO.cleanup(7)

# st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 1400, 30))
# st1.start()
# st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 1400, 30))
# st2.start()

# st1.join()
# st2.join()
# st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 500, 30))
# st2.start()
# st2.join()
# st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 500, 15))
# st2.start()

# calibrate(myStepper1)
# calibrate(myStepper2)

print "Ik ben hier"
print pos_x
print pos_y
