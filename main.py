#!/usr/bin/env python3.5
import cv2
import os 
import sys
import uuid
from helpers import Helpers
helpers = Helpers()

# Open image
imagePath = sys.argv[1]
imageCv = helpers.openImageCv(imagePath)

# Pre-processing
gray = helpers.cvToGrayScale(imageCv)
bilateral = helpers.cvApplyBilateralFilter(gray)
blur = helpers.cvApplyGaussianBlur(bilateral, 5)

# Detect edge contours, and find the plate contour
edged = helpers.cvToCannyEdge(blur)
contours = helpers.cvExtractContours(edged)
rectangleContours = helpers.cvFilterRectangleContours(contours)
plateContour = rectangleContours[0]
plateContour = helpers.cvResizeContour(plateContour, 1.0)

# Crop and blur the plate
plateImage = helpers.cvCropByContour(imageCv, plateContour)
plateImageBlur = helpers.cvApplyGaussianBlur(plateImage, 25)

# Find the plate's background color
plateBackgroundColor = helpers.cvFindMostOccurringColor(plateImageBlur)

# Draw over the plate
result = cv2.drawContours(imageCv.copy(), [plateContour], -1, plateBackgroundColor, -1)

# Show results
#cv2.imshow('Original Image', imageCv)
#cv2.imshow('Result', result)


plateblurimage1 = str(uuid.uuid4())
plateblurimage2 = ".jpg"
plateblurimagefilename = "".join((plateblurimage1, plateblurimage2))
cv2.imwrite('./modifiedimage/'+plateblurimagefilename, result)
print("blurred via python: <img src='./modifiedimage/"+plateblurimagefilename+"' width='50%'>")

cv2.waitKey()