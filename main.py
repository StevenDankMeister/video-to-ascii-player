import os
import time
import re
import math
import cv2
import shutil
import colorama
import imutils
import numpy as np
import sys
from PIL import Image

video_frames = []

def extractFramesFromVideo(video_path, temp_location):
    print('[1] Processing video.')
    video = cv2.VideoCapture(video_path)
    if os.path.exists(temp_location):
        print('Temp directory already exists. Move or delete it.')
        return (False, 0)
    framerate = video.get(cv2.CAP_PROP_FPS)
    
    i = 1
    while(video.isOpened()):
        ret, frame = video.read()
        if ret == False:
            return (True, framerate)
        dimension = os.get_terminal_size()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (dimension.columns - 1, dimension.lines), interpolation=cv2.INTER_AREA)
        #cv2.imwrite(temp_location+str(i)+'.jpg', frame)
        video_frames.append(frame)
        print('\r        Processed frame: '+str(i), end='')
        i+=1

    video.release()
    cv2.destroyAllWindows()

def processFrames(frames_dir):
    print('\n[2] Processing frames.')
    frames = []
    images = video_frames

    brightness = ' .:-=+*#%@'
    count = 0
    for image in images:
        frame = ''
        im = Image.fromarray(image)
        width, height = im.size
        for y in range(height):
            for x in range(width):
                pixel_brightness = im.getpixel((x,y))
                index = math.floor(pixel_brightness/255 * (len(brightness)-1))
                frame += brightness[index]
            frame+='\n'

        frames.append(frame)
        
        count += 1

        percentage = int(math.ceil(count / len(images) * 100))
        bar = str.format('\r        Progress '+str(percentage)+'%: [{}{}] | {} of {}', '#'*(int(percentage/5)), '='*(20-int(percentage/5)), count, len(images))
        print(bar, end='')

    return frames


def main():
    current_directory = os.getcwd()
    temp_directory = current_directory+'\\temp\\'
    video_file_name = input("Enter file name: ")
    
    ret, framerate = extractFramesFromVideo(current_directory+'/'+video_file_name, temp_directory)
    frametime = 1/(framerate)

    if ret == False:
        return

    frames = processFrames(temp_directory)

    input("\nPress any key to play")
    start = time.time()
    elapsed_time_start = start
    i = 0
    #MUCH FASTER and more accurate than time.sleep
    while i < len(frames):
        now = time.time()
        if (now - start) > frametime:
            start = time.time()
            print(frames[i], end="")
            i += 1
            
    elapsed_time_end = time.time()
    print("\nElapsed time: ", (elapsed_time_end - elapsed_time_start))

if __name__ == "__main__":
    main()
