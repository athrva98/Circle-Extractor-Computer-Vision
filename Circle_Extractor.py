# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 23:05:30 2021

@author: Athrva Pandhare
"""

import numpy as np 
import matplotlib.pyplot as plt 
import cv2 
def adaptiveThreshold(img,  sub_thresh = 0.10):
    image = img.copy()
    if image.shape[-1] == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray_image = image
    integralimage = cv2.integral(gray_image, cv2.CV_32F)
    
    width = gray_image.shape[1]
    height = gray_image.shape[0]
    win_length = int(width / 10)
    image_thresh = np.zeros((height, width, 1), dtype = np.uint8)
    for j in range(height):
        for i in range(width):
            x1 = i - win_length
            x2 = i + win_length
            y1 = j - win_length
            y2 = j + win_length
            if(x1 < 0):
                x1 = 0
            if(y1 < 0):
                y1 = 0
            if(x2 > width):
                x2 = width -1
            if(y2 > height):
                y2 = height -1
            count = (x2- x1) * (y2 - y1)

#            I(x,y) = s(x2,y2) - s(x1,y2) - s(x2, y1) + s(x1, y1)
            sum = integralimage[y2, x2] - integralimage[y1, x2] -integralimage[y2, x1] +integralimage[y1, x1]
            if (int)(gray_image[j, i] * count) < (int) (sum * (1.0 - sub_thresh)):
                image_thresh[j, i] = 0
            else:
                image_thresh[j, i] = 255

    return image_thresh

image = cv2.imread(r'C:\Users\Athrva Pandhare\Desktop\New folder (3)\Hands-On-Computer-Vision-with-OpenCV-4-Keras-and-TensorFlow-2-master\pipes2.jpg') 
image = cv2.resize(image, (700,700), cv2.INTER_CUBIC)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
r = cv2.selectROI("Display_ROI",image)
cv2.waitKey(0)
        
    
image = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
pixel_vals = image.reshape((-1,3)) 
 
pixel_vals = np.float32(pixel_vals)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.75) 

k = 3
retval, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS) 

centers = np.uint8(centers) 
segmented_data = centers[labels.flatten()] 

segmented_image = segmented_data.reshape((image.shape)) 

mask = np.zeros(segmented_image.shape[:2], dtype = np.uint8)
segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)
segmented_image = adaptiveThreshold(segmented_image)
plt.imshow(segmented_image)
contours, hierarchy = cv2.findContours(segmented_image,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
approx = []
for cnt in contours[1:]:
    epsilon = 0.0001*cv2.arcLength(cnt,True)
    approx.append(cv2.approxPolyDP(cnt,epsilon,True))
    try:
        ellipse = cv2.fitEllipse(cnt)
        (x,y),(MA,ma),angle = ellipse
        MA = max(MA, ma)
        area = cv2.contourArea(cnt)
        equi_diameter = np.sqrt(4*area/np.pi)
        print(MA/equi_diameter)
        if MA/equi_diameter < 1.5 and MA < max(mask.shape)/1.7:
            img = cv2.ellipse(mask,ellipse,(255,255,255),3)
    except:
        print("moving on...")

cv2.imshow("contours : ",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

