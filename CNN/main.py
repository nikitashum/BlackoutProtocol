from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import tensorflow as tf
import socket

# socket settings
TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establish socket connection
try:
    s.connect((TCP_IP, TCP_PORT))
    print("Transmitting on: " + TCP_IP + ":" + str(TCP_PORT))
except Exception as e:
    print(e)


# method for drawing a frame around face and displaying prediction
def draw_frame(res, fra):
    # loop over the results
    for r in res:
        # draw the bounding box of the face along with the associated
        # predicted age
        text = "{}: {:.2f}%".format(r["cat"][0], r["cat"][1] * 100)
        (startX, startY, endX, endY) = r["loc"]
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(fra, (startX, startY), (endX, endY),
                      (0, 0, 255), 2)
        cv2.putText(fra, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        return fra


# method for predicting face and situation
def predict_case(frame, faceNet, model, minConf=0.5):
    # define the list of categories
    CATEGORIES = ['Normal', 'Distracted', 'Tired']

    # initialize our results list
    results = []

    # grab the dimensions of the frame and then construct a blob from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > minConf:
            # compute the (x, y)-coordinates of the bounding box for teh object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the ROI of the face
            face = frame[startY:endY, startX:endX]

            # ensure the face ROI is sufficiently large
            if face.shape[0] < 20 or face.shape[1] < 20:
                continue

            # construct a blob from *just* the face ROI
            faceBlob = cv2.dnn.blobFromImage(face, 1.0, (200, 200),
                                             (78.4263377603, 87.7689143744, 114.895847746),
                                             swapRB=False)

            # make predictions on the situation and
            # output the largest corresponding probability
            preds = model.predict(faceBlob)
            i = preds[0].argmax()
            cat = CATEGORIES[i]
            confidence = preds[0][i]

            # construct a dictionary consisting of both the face
            # bounding box location along with the situation prediction,
            # then update our results list
            d = {
                "loc": (startX, startY, endX, endY),
                "cat": (cat, confidence, i)
            }
            results.append(d)

    # return our results to the calling function
    return results


# method for encoding result to bytes and sending it over TCP socket
def sendResult(result):
    for r in result:
        result = ("CNN" + str(r["cat"][2]))
        resultInBytes = str(result).encode('utf-8')
        try:
            s.send(resultInBytes)
        except Exception as e:
            print(e)
        return


# main variables
mainLoop = True
prototxtPath = "CNN/face_detector/deploy.prototxt"
weightsPath = "CNN/face_detector/res10_300x300_ssd_iter_140000.caffemodel"  # Face recognition model
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
# trained cnn model made by BlackoutProtocol team
model = tf.keras.models.load_model('CNN/10-conv-50-nodes-1-dense1589459059')
DEFAULT = "CNN/images/Normal/22b.jpg"  # Default image (Normal)
frame = cv2.imread(DEFAULT)  # init frame with default image

# main loop
while mainLoop:

    # method for displaying normal situation
    def normal():
        return cv2.imread(DEFAULT)  # Normal face expression

    # method for displaying distracted situation
    def distracted():
        return cv2.imread("CNN/images/Distracted/images1.jpg")  # Distracted

    # method for displaying tired situation
    def tired():
        return cv2.imread("CNN/images/Tired/images7.jpg")  # Tired face

    # method for starting and displaying webcam feed
    def webcam():  # Webcam live feed
        innerLoop = True
        # initialize the video stream
        vs = VideoStream(src=0).start()
        # warm video sensors
        time.sleep(2.0)

        # loop over the frames from the video stream
        while innerLoop:
            global frame
            global results
            global key
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            # detect faces in the frame, and for each face in the frame
            results = predict_case(frame, faceNet, model)
            # transmit result
            sendResult(results)
            # draw the box around the face and display prediction
            newFrame = draw_frame(results, frame)
            # show the output frame
            try:
                cv2.imshow("Frame", newFrame)
            except Exception as e:
                # show webcam frame if no face detected
                cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop and turn of camera
            if key == ord("q"):
                innerLoop = False
                vs.stop()
        return cv2.imread(DEFAULT)  # Switch back to default image

    # switch case for switching situation
    def switch(i):
        switcher = {
            0: normal,
            1: webcam,
            2: distracted,
            3: tired
        }
        func = switcher.get(i, lambda: 'Invalid')
        return func()

    # resize frame to have a maximum width of 400 pixels
    frame = imutils.resize(frame, width=400)
    # detect faces in the frame, and for each face in the frame
    results = predict_case(frame, faceNet, model)
    # transmit result over TCP socket
    sendResult(results)
    # draw the box around the face and display prediction
    frame = draw_frame(results, frame)
    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(0) & 0xFF
    # keyboard controls for switch case
    if key == ord("w"):
        frame = switch(1)

    elif key == ord("q"):
        mainLoop = False
        cv2.destroyAllWindows()

    elif key == ord("d"):
        frame = switch(2)

    elif key == ord("t"):
        frame = switch(3)

    else:
        frame = switch(0)

s.close()
