import RPi.GPIO as GPIO
import time
import datetime
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

Pdir = 14
Pstep = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(Pdir, GPIO.OUT)
GPIO.setup(Pstep, GPIO.OUT)

db_url = "https://recyclear-user-c81c3-default-rtdb.asia-southeast1.firebasedatabase.app/"
cred = credentials.Certificate("firebase.json")
default_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})

ref = db.reference("Detect").child("Class")


def move(degree, degreeTime):
    if degree > 0:
        GPIO.output(Pdir, GPIO.LOW)

    else:
        GPIO.output(Pdir, GPIO.HIGH)

    if degree != 0:
        degree = abs(degree)
        nstep = degree / 1.8
        pulse = degreeTime / nstep / 2

        for i in range(int(nstep)):
            GPIO.output(Pstep, GPIO.HIGH)
            time.sleep(pulse)
            GPIO.output(Pstep, GPIO.LOW)
            time.sleep(pulse)


curClass = 0
prevClass = 0

while True:
    curClass = (int)(ref.get()) % 5
    diffClass = curClass - prevClass
    print(datetime.datetime.now(), 'Waiting for Detecting ... Current Class %d' % curClass)

    if diffClass != 0:
        if diffClass > 2:
            diffClass -= 5
        if diffClass < -2:
            diffClass += 5

        move(diffClass * 72, abs(diffClass) * 0.45)
        prevTime = time.time()
        prevClass = curClass
        print('Current Class: ', curClass)
