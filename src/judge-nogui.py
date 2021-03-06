#! /usr/bin/env python

import sys
import time
import math
import numpy as np
from scipy.interpolate import UnivariateSpline 
import cv2
import cv2.cv as cv
import mraa


# Function to map the value between two ranges
def range_map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# For the prototype, we hardcode the line position.
# Later on we can determine it automatically using hough lines
line_x = int((640 * 2) / 2)

wnd_caption = 'Ball tracking'
mirror_trajectory = True
trajectory_x = []
trajectory_y = []
trajectory_r = []
frame = None
first_frame = None
frame_w = 0
frame_h = 0
frame_count = 10
hsv = None
color_distance = 1.0 - 0.50
hsv_avg = np.array([range_map(56, 0, 360, 0, 180), 
                    range_map(34, 0, 100, 0, 255), 
                    range_map(93, 0, 100, 0, 255)], 
                   np.uint8)

# Setup GPIO pins for LEDs
led_in = mraa.Gpio(14)
led_in.dir(mraa.DIR_OUT)
led_out = mraa.Gpio(15)
led_out.dir(mraa.DIR_OUT)


if len(sys.argv) == 2:
    video_file = sys.argv[1]
else:
    print('Usage: ./judge.py <video_file_name>')
    print('using ../data/video/fuerte/side4.mkv as video_file_name')
    video_file = '../data/video/fuerte/side4.mkv'

fgbg = cv2.BackgroundSubtractorMOG2(bShadowDetection=False, 
                                    history=20, 
                                    varThreshold=64)
cap = cv2.VideoCapture(video_file)
ret = True

if not cap.isOpened():
    print('Can not open capturing device')
    sys.exit(1)

while(ret and frame_count > 0):

    ret, raw_frame = cap.read()

    if ret == False or raw_frame is None:
        print('Capturing error')
        break
    else:
        # upscale frame
        frame = cv2.pyrUp(raw_frame)

        fgmask = fgbg.apply(frame)

        # Remove noise from backgound mask (low pass filter)
        kernel_size = 7
        fgmask = cv2.medianBlur(fgmask, kernel_size)
        fgmask = cv2.inRange(fgmask,
                             np.array((210), np.uint8),
                             np.array((255), np.uint8))

        # Apply foreground mask to cut out static parts
        fg_frame = cv2.bitwise_and(frame, frame, mask=fgmask)

        hsv = cv2.cvtColor(fg_frame, cv2.COLOR_BGR2HSV)
        # Generate mask
        k1 = color_distance
        k2 = 1 + (1 - k1)
        mask = cv2.inRange(hsv, 
                           np.array([min(180, int(hsv_avg[0] * k1)), min(255, int(hsv_avg[1] * k1)), min(255, int(hsv_avg[2] * k1))], np.uint8),
                           np.array([min(180, int(hsv_avg[0] * k2)), min(255, int(hsv_avg[1] * k2)), min(255, int(hsv_avg[2] * k2))], np.uint8)
        )
    

        # Hough circle detection
        hough_in = cv2.GaussianBlur(fgmask, (3, 3), 0)
        circles = cv2.HoughCircles(image=hough_in, 
                                   method=cv.CV_HOUGH_GRADIENT, 
                                   dp=1, minDist=50,#minDist=h / 10, 
                                   # type, 1/scale, min center dists
                                   param1=200, param2=9, # params1?, param2?
                                   minRadius=3, maxRadius=15) # min radius, max radius

        if circles is not None and len(circles) > 0:
            # Fancy up output
            cc = circles[0].tolist()
            cc = [cc[0]]
            
            first = True
            for (x, y, radius) in cc:
                x = int(round(x))
                y = int(round(y))
                radius = int(round(radius))
                print((x, y, radius))
                if first:
                    frame_count -= 1
                    #cv2.circle(frame, (x,y), radius, cv.CV_RGB(255,0,0), 2, cv.CV_AA, 0)
                    if first_frame is None:
                        first_frame = frame
                        (frame_h, frame_w, _) = frame.shape

                    trajectory_x.append(x)
                    trajectory_y.append(y)
                    trajectory_r.append(radius)
                    first = False
                else:
                    #cv2.circle(frame, (x,y), radius, cv.CV_RGB(0,0,255), 2, cv.CV_AA, 0)
                    pass

if cap.isOpened():
    cap.release()

if len(trajectory_x) < 2:
    print('Ball is not detected')
    sys.exit(2)
    
if mirror_trajectory == True:
    trajectory_x.reverse()
    trajectory_y.reverse()
    trajectory_r.reverse()

bounce_idx = 0

# Find the trajectory element with minimal y
val, bounce_idx = max((val, idx) for (idx, val) in enumerate(trajectory_y))

for i in range(0, len(trajectory_x)):
    if i < bounce_idx:
        circle_color = cv.CV_RGB(0,0,255)
    else:
        circle_color = cv.CV_RGB(255,0,0)
        
    cv2.circle(first_frame, 
               (trajectory_x[i], trajectory_y[i]), 
               trajectory_r[i],
               circle_color,
               2, 
               cv.CV_AA, 
               0)


before_bounce = UnivariateSpline(trajectory_x[:bounce_idx], trajectory_y[:bounce_idx])
x0 = trajectory_x[0]
x1 = x0
y0 = before_bounce(x0)
while x0 < trajectory_x[bounce_idx]:    
    x1 += 1
    y1 = before_bounce(x1)
    cv2.line(first_frame, (x0, y0), (x1, y1), cv.CV_RGB(0,255,0), thickness = 2)
    x0 = x1
    y0 = y1

after_bounce = UnivariateSpline(trajectory_x[bounce_idx:], trajectory_y[bounce_idx:])
x0 = trajectory_x[bounce_idx - 1]
x1 = x0
y0 = after_bounce(x0)
while x0 < trajectory_x[-1]:    
    x1 += 1
    y1 = after_bounce(x1)
    cv2.line(first_frame, (x0, y0), (x1, y1), cv.CV_RGB(0,255,0), thickness = 2)
    x0 = x1
    y0 = y1

x_cross = trajectory_x[bounce_idx - 1]
while abs(before_bounce(x_cross) - after_bounce(x_cross)) > 0.01 and x_cross < trajectory_x[bounce_idx]:
    x_cross += 0.01

cv2.circle(first_frame, 
           (int(x_cross), int(before_bounce(x_cross))), 
           3,
           cv.CV_RGB(255,255,0),
           2, 
           cv.CV_AA, 
           0)

(rows, cols, _) = first_frame.shape

# Switch corresponding LED
if x_cross > line_x:
    print('IN')
    led_in.write(1)
    led_out.write(0)
else:
    print('OUT')
    led_in.write(0)
    led_out.write(1)

# Wait 3 seconds and turn all LEDs off
time.sleep(3)
led_in.write(0)
led_out.write(0)
