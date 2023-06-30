from PIL import Image
from moviepy.editor import VideoFileClip
import time
import cv2
import os, random

basedir = os.path.abspath(os.path.dirname(__file__))

def getFrameImage(videoFile):
    start = time.perf_counter()
    vid = VideoFileClip(videoFile)
    images = []
    for i in range(0, vid.reader.nframes):
        img = Image.fromarray(vid.get_frame(i))
        images.append(img)
    end = time.perf_counter()
    print(end-start)
    return images

def getFrameCv(video):
    start = time.perf_counter()
    vid = cv2.VideoCapture('test.mp4')
    count = 0
    success = 1
    data = []
    while success:
        success, image = vid.read()
        cv2.imwrite('test/t/frame%d.jpg' %count, image)
        count+=1
    end = time.perf_counter()
    print(end-start)
    return data

# def getFrameImage(video):
#     vid = cv2.VideoCapture(video)
#     count = 0
#     success = 1
#     dirName = 'runs/ext%d'%random.randint(0,1000)
#     os.mkdir(dirName)
#     data = []
#     while success:
#         success, image = vid.read()
#         cv2.imwrite(dirName+'frame%d.jpg' %count, image)
#         data.append[dirName+'/frames%d.jpg'%count]
#         count+=1
    
#     return data

def getFrameImage(video):
    vid = cv2.VideoCapture(video)
    count = 0
    success = 1
    dirName = basedir+'/.ipynb/runs/ext%d'%random.randint(0,1000)
    os.mkdir(dirName)
    print(dirName)
    numFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    data = []
    while count<numFrames:
        success, image = vid.read()
        cv2.imwrite(os.path.join(dirName, 'frame%d.jpg' %count), image)
        fname = str(dirName)+'/frames'+str(count)+'.jpg'
        data.append(fname)
        count+=1
    
    return data



                   
##data = getFrameImage('test.mp4')
data = getFrameImage('test.mp4')
