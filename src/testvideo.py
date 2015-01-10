#! /usr/bin/env python

import sys
import numpy as np
import cv2

# cv2.VideoCapture can use file and camera as a video source.
# If string is passed to constructor, then input is treated as
# file. If integer is passed, then corresponding connected camera will
# be used, i.e. 0 is /dev/video0, 1 is /dev/video1, etc.

if len(sys.argv) == 2:
    if f[:-1] == '/dev/video':
        # use camera for capture
        video_file = int(f[10:])
    else:
        # using file as an input
        video_file = f
    
else:
    print('Usage: ./testvideo.py <video_file_name>')
    print('using /dev/video0 as video_device_file_name')
    video_file = 0

cap = cv2.VideoCapture(video_file)

ret = True
while(ret and cap.isOpened()):
    ret, frame = cap.read()

    if ret and frame is not None:
        # Make frame grayscale
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('frame', gray)

        # Draw red dot in top right corner to test how frames are
        # accessible as numpy arrays
        frame[10][10] = (0, 0, 255) # OpenCV uses BGR
        
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)

cap.release()

cv2.destroyAllWindows()
