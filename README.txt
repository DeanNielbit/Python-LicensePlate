###################################################
//HOW TO USE
###################################################

REQUIRED INSTALL PYTHON
now for webbrowser ready

#TERMINAL
###################################################
pip install opencv-python
pip install opencv-python-headless
pip install opencv-contrib-python
pip install numpy
pip install image


#USAGE
###################################################
#step_6_retrieve_plate_image.py - to see only numberplate change
#main.py - to run full script - put file name in here


#TUTORIAL
###################################################
To break down the algorithm before we start coding:
* Detect where the license plate is located on our input image
* Approximate license plate’s background color
* Fill the license plate with the color we calculated
    

We will need to open it as PIL image first, and then we can convert it to the OpenCV format:

//------------------------------------------------CODE----------------------------------------------------
from PIL import Image as imageMain
from PIL.Image import Image
import cv2
import numpy

imagePath = './image/image1.jpg'
imagePil = imageMain.open(imagePath)
imageCv = cv2.cvtColor(numpy.array(imagePil), cv2.COLOR_RGB2BGR)
cv2.imshow('Original Image', imageCv)
//------------------------------------------------CODE----------------------------------------------------


Now we’ll need to apply some pre-processing in OpenCV to make contour detection work. Namely we convert the image to gray scale, apply bilateral filter with cv2.bilateralFilter and Gausian blur with cv2.GaussianBlur:


//------------------------------------------------CODE----------------------------------------------------
gray = cv2.cvtColor(imageCv, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray Scaled', gray)

bilateral = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow('After Bilateral Filter', bilateral)

blur = cv2.GaussianBlur(bilateral, (5, 5), 0)
cv2.imshow('After Gausian Blur', blur)
//------------------------------------------------CODE----------------------------------------------------


With this pre-processing completed, we can do a canny edge detection using cv2.Canny, find all contours with cv2.findContours, and examine 30 largest ones:


//--------------------------------------------------------CODE------------------------------------------------------------
edged = cv2.Canny(blur, 170, 200)
cv2.imshow('After Canny Edge', edged)

contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]
tempContours1 = cv2.drawContours(imageCv.copy(), contours, -1, (255, 0, 0), 2)
cv2.imshow('Detected Contours', tempContours1)
//------------------------------------------------CODE----------------------------------------------------

Now we can find only contours that are shaped like rectangles. To do that we go through each contour, calculate the perimeter with cv2.arcLength, and approximate the contour using cv2.approxPolyDP, with approximation accuracy (maximum distance between the original contour and its approximation) taken as 2% of perimeter. If the resulting approximated figure has exactly 4 points (i.e. resembles a rectangle) it might be our license plate. And since we start from the largest contour — license plate should be the first rectangle contour we found:

//------------------------------------------------CODE----------------------------------------------------
rectangleContours = []
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approximationAccuracy = 0.02 * perimeter
    approximation = cv2.approxPolyDP(contour, approximationAccuracy, True)
    if len(approximation) == 4:
        rectangleContours.append(contour)
        
plateContour = rectangleContours[0]
tempContours2 = cv2.drawContours(imageCv.copy(), [plateContour], -1, (255, 0, 0), 2)
cv2.imshow('Detected Plate Contour', tempContours2)
//------------------------------------------------CODE----------------------------------------------------

Now to determining the plate’s background color. First retrieve the plate’s image using cv2.boundingRect over the contour, and apply some hard blur to minimize noise:

//------------------------------------------------CODE----------------------------------------------------
x,y,w,h = cv2.boundingRect(plateContour)
plateImage = imageCv[y:y+h, x:x+w]
cv2.imshow('Plate Original', plateImage)

plateImageBlur = cv2.GaussianBlur(plateImage, (25, 25), 0)
cv2.imshow('Plate Blurred', plateImageBlur)
//------------------------------------------------CODE----------------------------------------------------

After the license plate was separated from the main image we can analyze its colors and determine the most dominant BGR color in it:

//------------------------------------------------CODE----------------------------------------------------
def findMostOccurringColor(cvImage) -> (int, int, int):
    width, height, channels = cvImage.shape
    colorCount = {}
    for y in range(0, height):
        for x in range(0, width):
            BGR = (int(cvImage[x, y, 0]), int(cvImage[x, y, 1]), int(cvImage[x, y, 2]))
            if BGR in colorCount:
                colorCount[BGR] += 1
            else:
                colorCount[BGR] = 1

    maxCount = 0
    maxBGR = (0, 0, 0)
    for BGR in colorCount:
        count = colorCount[BGR]
        if count > maxCount:
            maxCount = count
            maxBGR = BGR

    return maxBGR

plateBackgroundColor = findMostOccurringColor(plateImageBlur)
tempContours3 = cv2.drawContours(imageCv.copy(), [plateContour], -1, plateBackgroundColor, -1)
cv2.imshow('Original Image', imageCv)
cv2.imshow('Result', tempContours3)
//------------------------------------------------CODE----------------------------------------------------


That’s it! With the plate contour now filled by its background color we have a more-or-less working example of license plate remover.


#PITFALLS
###################################################
What if the car and the license plate has the same color (i.e. white)?
What if there are some rectangle signs on the picture? 
What if we have several cars in one picture, and we want to hide all their plates? 
What if the plate is only partially visible, but we still need to hide it? 
What if the plate is under some weird angle? 


#CONCLUSION
###################################################
We can’t handle all these cases relying purely on OpenCV. But it sure was fun to play around and build this solution.
