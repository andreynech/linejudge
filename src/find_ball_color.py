#! /usr/bin/env python

import sys
import time
import numpy as np
import cv2
import cv2.cv as cv


def range_map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


rx1 = -1
ry1 = -1
rx2 = -1
ry2 = -1
frame = None
hsv = None
#hsv_avg = np.array([range_map(44, 0, 360, 0, 180), range_map(35, 0, 100, 0, 255), range_map(63, 0, 100, 0, 255)], np.uint8)
#hsv_avg = np.array([18, 90, 168], np.uint8)
#hsv_avg = np.array([range_map(65, 0, 360, 0, 180), range_map(36, 0, 100, 0, 255), range_map(60, 0, 100, 0, 255)], np.uint8)
hsv_avg = np.array([range_map(56, 0, 360, 0, 180), range_map(34, 0, 100, 0, 255), range_map(93, 0, 100, 0, 255)], np.uint8)
print('Default average:', hsv_avg)
color_distance = 1.0 - 0.50


def mouseLeftDown(x, y, flags, param):
    global rx1, ry1, rx2, ry2
    rx1 = x
    ry1 = y
    rx2 = -1
    ry2 = -1
    

def mouseLeftUp(x, y, flags, param):
    global rx1, ry1, rx2, ry2, hsv_avg

    sel = hsv[rx1:rx2, ry1:ry2]
    sel = hsv[ry1:ry2, rx1:rx2]
    #hsv_avg = np.average(np.average(int(sel), axis=0), axis=0)
    hsv_avg = cv2.mean(sel)[:-1]

    print(hsv_avg)
    
    rx1 = -1
    ry1 = -1
    rx2 = -1
    ry2 = -1

    
def mouseMove(x, y, flags, param):
    global rx1, ry1, rx2, ry2
    rx2 = x
    ry2 = y

    
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseLeftDown(x, y, flags, param)
    elif event == cv2.EVENT_LBUTTONUP:
        mouseLeftUp(x, y, flags, param)
    elif event == cv2.EVENT_MOUSEMOVE:
        mouseMove(x, y, flags, param)


def new_distance(x):
    global color_distance
    color_distance = 1.0 - float(x) / 100
    

def cvOpen(src, dst, element):
    cv2.erode(src, element, dst)
    cv2.dilate(src, element, dst)


def cvClose(src, dst, element):
    cv2.dilate(src, element, dst)
    cv2.erode(src, element, dst)


if len(sys.argv) == 2:
    video_file = sys.argv[1]
else:
    print('Usage: ./testvideo.py <video_file_name>')
    print('using ../data/video/fuerte/front1.mkv as video_file_name')
    video_file = '../data/video/fuerte/front1.mkv'

cap = cv2.VideoCapture(video_file)
#fgbg = cv2.BackgroundSubtractorMOG()
#fgbg = cv2.BackgroundSubtractorMOG2()
fgbg = cv2.BackgroundSubtractorMOG2(bShadowDetection=False, history=20, varThreshold=64) # default threshold is 16
ret = True
stop_frame = False
cv2.namedWindow('frame', cv2.CV_WINDOW_AUTOSIZE)
cv2.setMouseCallback('frame', mouse_callback)

cv2.createTrackbar('Distance','frame', int((1.0 - color_distance) * 100), 100, new_distance)

while(ret and cap.isOpened()):

    if stop_frame == False:
        ret, raw_frame = cap.read()

    if ret and raw_frame is not None:
        #frame[10][10] = (0, 0, 255) # BGR - draw red dot in top right corner

        # upscale frame
        (rows, cols, depth) = raw_frame.shape
        frame = cv2.pyrUp(raw_frame)

        fgmask = fgbg.apply(frame)

        # Remove noise from backgound mask (low pass filter)
        kernel_size = 7
        #kernel = np.ones((kernel_size, kernel_size), np.float32) / kernel_size / kernel_size
        #fgmask = cv2.filter2D(fgmask, -1, kernel)
        fgmask = cv2.medianBlur(fgmask, kernel_size)
        #fgmask = cv2.bilateralFilter(fgmask, 17, 75, 75)
        fgmask = cv2.inRange(fgmask, 210, 255)
        
        fg_frame = cv2.bitwise_and(frame, frame, mask=fgmask)

        (h, w, ch) = frame.shape
        hsv = cv2.cvtColor(fg_frame, cv2.COLOR_BGR2HSV)
        # Generate mask
        k1 = color_distance
        k2 = 1 + (1 - k1)
        mask = cv2.inRange(hsv, 
                           np.array([min(180, int(hsv_avg[0] * k1)), min(255, int(hsv_avg[1] * k1)), min(255, int(hsv_avg[2] * k1))], np.uint8),
                           np.array([min(180, int(hsv_avg[0] * k2)), min(255, int(hsv_avg[1] * k2)), min(255, int(hsv_avg[2] * k2))], np.uint8)
        )
    
        # Perform morphological ops
#        se21 = cv2.getStructuringElement(cv.CV_SHAPE_RECT, (21, 21), (6, 6))
#        se11 = cv2.getStructuringElement(cv.CV_SHAPE_RECT, (11, 11), (5, 5))
#        cvClose(mask, mask, se21);
#        cvOpen(mask, mask, se11);
        se21 = cv2.getStructuringElement(cv.CV_SHAPE_RECT, (11, 11), (4, 4))
        se11 = cv2.getStructuringElement(cv.CV_SHAPE_RECT, (5, 5), (3, 3))
        cvClose(mask, mask, se21);
        cvOpen(mask, mask, se11);

        if rx1 != -1 and rx2 != -1:
            cv2.rectangle(hsv, (rx1, ry1), (rx2, ry2), cv.Scalar(0, 0, 255))


        # Hough transform
        hough_in = cv2.GaussianBlur(fgmask, (3, 3), 0)
        circles = cv2.HoughCircles(image=hough_in, 
                                   method=cv.CV_HOUGH_GRADIENT, 
                                   dp=1, minDist=50,#minDist=h / 10, 
                                   # type, 1/scale, min center dists
                                   param1=500, param2=15, # params1?, param2?
                                   minRadius=3, maxRadius=15) # min radius, max radius

        if circles is not None and len(circles) > 0:
            # Fancy up output
            cc = circles[0].tolist()
            cc = [cc[0]]
            #cc.sort(key=lambda x: x[2], reverse=True)
            
            first = True
            for (x, y, radius) in cc:
                x = int(round(x))
                y = int(round(y))
                radius = int(round(radius))
                #if fgmask[y][x] < 1:
                #    continue
                print((x, y, radius))
                #cv2.circle(frame, (x,y), 3, cv.CV_RGB(255,0,0), -1, cv.CV_AA, 0)
                if first:
                    cv2.circle(frame, (x,y), radius, cv.CV_RGB(255,0,0), 2, cv.CV_AA, 0)
                    first = False
                else:
                    cv2.circle(frame, (x,y), radius, cv.CV_RGB(0,0,255), 2, cv.CV_AA, 0)
                #cv2.circle(frame, (x,y), 3, cv.CV_RGB(0,255,0), -1, cv.CV_AA, 0)
                #cv2.circle(frame, (x,y), radius, cv.CV_RGB(255,0,0), 2, cv.CV_AA, 0)


        # Hough lines
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_frame, 50, 175, apertureSize = 3)

        lines = cv2.HoughLinesP(edges, 1, np.pi / 90, 80, minLineLength = 30, maxLineGap = 30)
        if lines is not None and len(lines) > 0:
            for line in lines[0]:
                cv2.line(frame, (line[0], line[1]), (line[2], line[3]), cv.CV_RGB(0,255,0), thickness = 2)



        cv2.imshow('frame', frame)
        #cv2.imshow('mask', mask)
        #cv2.imshow('hough_in', hough_in)
        #cv2.imshow('fgmask', fgmask)
        #cv2.imshow('edges', edges)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
#    if stop_frame:
#        key = cv2.waitKey(1) & 0xFF
#        time.sleep(0.1)
#    else:
#        key = cv2.waitKey(0) & 0xFF    
#
#    if key == ord('q'):
#        break
#    elif key == ord('s'):
#        stop_frame = True


cap.release()
cv2.destroyAllWindows()

