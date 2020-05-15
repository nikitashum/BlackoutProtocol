import numpy as np
import os
import cv2
import random

DATADIR = "./images"
CATEGORIES = ['Normal', 'Distracted', 'Tired']

faceCascade = cv2.CascadeClassifier('./face_detector/haarcascade_frontalface_default.xml')

training_data = []


def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img))
                gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.5,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                # loop over the detections
                for (x, y, w, h) in faces:

                    # extract the ROI of the face
                    face = img_array[y:y+h, x:x+w]

                    # ensure the face ROI is sufficiently large
                    if face.shape[0] < 20 or face.shape[1] < 20:
                        continue

                    # construct a blob from *just* the face ROI
                    faceBlob = cv2.dnn.blobFromImage(face, 1.0, (200, 200),
                                                     (78.4263377603, 87.7689143744, 114.895847746),
                                                     swapRB=False)
                    training_data.append([faceBlob, class_num])
            except Exception as e:
                print(e)
                continue


def getTrainingData():
    X = []
    Y = []
    create_training_data()
    random.shuffle(training_data)

    for features, label in training_data:
        X.append(features)
        Y.append(label)

    X = np.array(X).reshape(-1, 3, 200, 200)
    Y = np.array(Y)
    print(len(X))
    return X, Y
