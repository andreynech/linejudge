#! /usr/bin/env python

import sys
import numpy as np
import cv2


if len(sys.argv) == 2:
    video_file = sys.argv[1]
else:
    print('Usage: ./testvideo.py <video_device_file_name>')
    print('using /dev/video0 as video_device_file_name')
    video_file = '/dev/video0'

cap = cv2.VideoCapture(video_file)

ret = True
while(ret and cap.isOpened()):
    ret, frame = cap.read()

    if ret and frame is not None:
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('frame', gray)
        frame[10][10] = (0, 0, 255) # BGR - draw red dot in top right corner
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)

cap.release()


cv2.destroyAllWindows()
