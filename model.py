
import numpy as np
import cv2 as cv
import os
import time
from PIL import Image

basedir = os.path.abspath(os.path.dirname(__file__))

class ObjectDetection:
    def __init__(self):
        # PROJECT_PATH = os.path.abspath(os.getcwd())
        # MODELS_PATH = os.path.join(PROJECT_PATH, "models")

        self.MODEL = cv.dnn.readNet(
            basedir+"/models/yolov4-tiny.weights",
            basedir+"/models/yolov4-tiny.cfg")

        self.CLASSES = []
        with open(basedir+"/models/coco.names", "r") as f:
            self.CLASSES = [line.strip() for line in f.readlines()]

        self.OUTPUT_LAYERS = [
            self.MODEL.getLayerNames()[i - 1] for i in self.MODEL.getUnconnectedOutLayers()
        ]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        self.COLORS /= (np.sum(self.COLORS**2, axis=1)**0.5/255)[np.newaxis].T

    def detectObj(self, snap):
        height, width, channels = snap.shape
        blob = cv.dnn.blobFromImage(
            snap, 1/255, (416, 416), swapRB=True, crop=False
        )

        self.MODEL.setInput(blob)
        outs = self.MODEL.forward(self.OUTPUT_LAYERS)

        # ! Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # * Object detected
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    # * Rectangle coordinates
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv.FONT_HERSHEY_PLAIN
        testLabel = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.CLASSES[class_ids[i]])
                testLabel.append(label)
                color = self.COLORS[i]
                cv.rectangle(snap, (x, y), (x + w, y + h), color, 2)
                cv.putText(snap, label, (x, y - 5), font, 2, color, 2)
        return snap, testLabel

# model = ObjectDetection()

# video = cv.VideoCapture('X:/Documents/4.2/kbs/assignment2/objectSearch/test.mp4')
# labels = ''
# count =0
# while video.isOpened():
#   ok, frame = video.read()
  
#   if not ok:
#     break
  
#   img, labels = model.detectObj(frame)

#   # Convert the ndarray to an OpenCV image
#   img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

#   # create a PIL Image object from the ndarray
#   img = Image.fromarray(img)

#   # display the image
#   img.show()  
#   if count == 1:
#     break
#   count+=1
#   # cv2_imshow(img)
#   # time.sleep(0.02)

# print(labels)


        