import socket
import os
import base64
import json
import time
import random
from picamera import PiCamera

#CoordPlacement

globCoords = "0,0"
globMovementThreshold = 1.5
globMovementThresholdAmount = 1
globMovementZoomThreshold = 3
globLostVisualThreshold = 5
globLastMovementCoordsX = 0
globLastMovementCoordsY = 0
globLastMovementTime = time.time()
globLastVisualTime = time.time()

def updateEye(coords):
    global globCoords, globMovementThreshold, globMovementThresholdAmount, globMovementZoomThreshold, globLostVisualThreshold, globLastMovementCoordsX, globLastMovementCoordsY, globLastMovementTime, globLastVisualTime
    text = coords
    pupilLevel = 0.4
    if(text != globCoords):
        globCoords = text
        globLastVisualTime = time.time()
        if abs(float(text.split(",")[0]) - globLastMovementCoordsX) > globMovementThresholdAmount or abs(float(text.split(",")[1]) - globLastMovementCoordsY) > globMovementThresholdAmount:
            globLastMovementTime = time.time()
            globLastMovementCoordsX = float(text.split(",")[0])
            globLastMovementCoordsY = float(text.split(",")[1])
    if(time.time() - globLastVisualTime > globLostVisualThreshold):
        #lost visual
        print("Lost visual")
        pupilLevel = 0.85
        newX = str(random.uniform(-20,20))
        newY = str(random.uniform(-20,20))
        text = newX+","+newY
    elif(time.time() - globLastMovementTime > globMovementThreshold):
        #move around a little randomly
        print("Moving a little randomly")
        pupilLevel = 0.15
        newX = str(float(text.split(",")[0])+random.uniform(-3,3))
        newY = str(float(text.split(",")[1])+random.uniform(-3,3))
        text = newX+","+newY

    #Write everything
    #print(text, pupilLevel)
    f = open("../coords.txt", "w")
    f.write(text)
    f.close()
    f = open("../pupil.txt", "w")
    f.write(str(pupilLevel))
    f.close()

#piCam
camera = PiCamera()
time.sleep(0.1)

BUFFER_SIZE = 4096

host = "10.0.0.1"
port = 5001

filename = "picture.jpg"
filesize = os.path.getsize(filename)

s = socket.socket()
while True:
    print("Trying to connect to "+host+":"+str(port))
    try:
        s.connect((host,port))
        print("Connected!")
        break
    except:
        time.sleep(5)

while True:
    try:
        camera.capture(filename)
    except:
        continue
    with open(filename, "rb") as f:
        fileData = f.read()
        fileData = base64.b64encode(fileData)
        fileData = json.dumps(fileData.decode())
        s.sendall(fileData.encode())
    response = s.recv(BUFFER_SIZE).decode()
    if(response != "None"):
        updateEye(response)
        print(response)
    else:
        updateEye(globCoords)
        print(response)
