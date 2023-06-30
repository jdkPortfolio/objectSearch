from flask import Flask, render_template, request, make_response
from pandas import array, read_pickle
from werkzeug.utils import secure_filename
from model import ObjectDetection
import json
from PIL import Image, ImageSequence, ImageTk
import os
import time, numpy as np
import cv2 as cv
import tkinter as tk
import imageio
import io
import base64

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

upFolder = os.path.join(basedir, 'static/runs/ext')
app.config['UPLOAD'] = upFolder

@app.route('/')
def hello_world():
    return render_template('choose.html')

@app.route('/groupMembers')
def viewMembers():
    return render_template('index.html')

@app.route('/objectSearch', methods= ['GET','POST'])
def objectSearch():
    videoFile = request.files['file']
    searchQuery = request.form['searchQuery']
    videoFile.save(secure_filename(videoFile.filename))

    model = ObjectDetection()
    frameLabels, originalFrames, contouredFrames, vidFps = frameProcessing(model, videoFile.filename)

    arrays, classes, success = combineRequest(frameLabels, originalFrames, contouredFrames, searchQuery)
    # print(classes)

    times = ''
    try:
        times = calculateTime(arrays, vidFps)
    except:
        pass
    
    if success == 1:
        try:
            # data = imageProcessing(arrays)
            return render_template('displaymod.html', images=classes, search=searchQuery, ref=times)
        except:
            return render_template('displaymod.html', images=classes)
    elif success == 0:
        return render_template('choosemod.html', classes=classes)



def frameProcessing(model, video):
    video = cv.VideoCapture(video)
    vidFps = video.get(cv.CAP_PROP_FPS)
    # print(g)
    frameLabels = {}
    originalFrames = []
    contouredFrames = []
    count = 0
    while video.isOpened():
        success, frame = video.read()

        if not success:
            break

        originalFrames.append(frame)
        img, labels = model.detectObj(frame)
        contouredFrames.append(img)
        frameLabels[count] = labels
        count+=1

    return frameLabels, originalFrames, contouredFrames, vidFps

def combineRequest(frameLabels, originalFrames, countouredFrames, searchQuery):
    detectedPositions = []
    for key in frameLabels:
        for item in frameLabels[key]:
            if searchQuery == item:
                detectedPositions.append(key)
    
    detectedPositions = list(set(detectedPositions))
    mixedFrames = []
    success = 0
    for i in range(0, originalFrames.__len__()):
        # done = 0
        try:
            for x in range(0, detectedPositions.__len__()):
                if i == detectedPositions[x]:
                    mixedFrames.append(countouredFrames[i])
                    success = 1
                    # done = 1
                    break
            # if done == 0:
            #     pass
            #     # mixedFrames.append(originalFrames[i])
        except:
            pass
        
    data = []
    for i in frameLabels:
        for x in frameLabels[i]:
            # print(x)
            data.append([x])
    data = list(set([item for sublist in data for item in sublist]))
        
    if detectedPositions.__len__() < 1:
        success = 0
        return data, data, success

    return detectedPositions, data, success

def videoProcessing(frames):
    output_file = 'output.mp4'
    frame_rate = 5

    video_writer = imageio.get_writer(output_file, fps=frame_rate)
    images = [Image.fromarray(i) for i in frames]

    # Write each image to the video file
    for image in images:
        video_writer.append_data(np.array(image))

    # Close the video writer object
    video_writer.close()


    return 'str(frames[0].__type__())'

def imageProcessing(frames):
    images = [Image.fromarray(i) for i in frames]
    result = []
    for i in range(0, images.__len__()):
        images[i].save(os.path.join(app.config['UPLOAD'], 'frame'+str(i)+'.png'))
        result.append('frame'+str(i)+'.png')
    # img_byte_arr = io.BytesIO()
    # for i in range(0, images.__len__()):
    #     images[i].save(img_byte_arr, format='PNG')
    #     img_byte_arr.seek(0)

    #     img_data = base64.b64decode(img_byte_arr.getvalue())
    
    #     # Create a response object that contains the image data
    #     # response = make_response(img_byte_arr.getvalue())
    #     # response.headers['Content-Type'] = 'image/jpeg'
    #     result.append(img_data)

    return result

def calculateTime(framePositions, videoFPS):
    tsecs = [i for i in framePositions]
    testt = [round(i+1/videoFPS,2) for i in tsecs]
    # round(i/videoFPS,2)
    print(testt)
    return testt

# def clearImageDir():

