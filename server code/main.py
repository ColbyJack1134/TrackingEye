import cv2
import socket
import json
import base64
#import requests
thres = 0.65 # Threshold to detect object

classNames = []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

#socket stuff
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

while True:
    try:
        s = socket.socket()
        s.bind((SERVER_HOST, SERVER_PORT))

        s.listen(1)
        print("Listening...")
        client_socket, address = s.accept()
        print(str(address)+" Connected")
        while True:
            with open("/var/www/html/images/captureEye.jpg", "wb") as f:
                finalData = ""
                while True:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if bytes_read == b'':
                        raise Exception("client disconnected")
                    finalData += bytes_read.decode()
                    try:
                        finalData = json.loads(finalData)
                        break
                    except:
                        pass
                finalData = base64.b64decode(finalData)
                f.write(finalData)

            dataToSend = "None"
            img = cv2.imread("/var/www/html/images/captureEye.jpg", cv2.IMREAD_COLOR)
            classIds, confs, bbox = net.detect(img,confThreshold=thres)

            if len(classIds) != 0:
                for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                    className = classNames[classId - 1]
                    if(className == "person"):
                        print(bbox)
                        arr = bbox[0]
                        x = arr[0]
                        y = arr[1]
                        width = arr[2]
                        height = arr[3]
                        dataToSend = str(float((x + width/2) * 60/640 - 30)) + "," + str(-1* float((y + height/2) * 60/480 - 30))
            print(dataToSend)
            client_socket.send(dataToSend.encode())
            #open("/var/www/html/images/coords.txt", "w").write(dataToSend)
    except KeyboardInterrupt:
        break
    except:
        print("EXCEPTION")
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            print("double exception")    
        continue
