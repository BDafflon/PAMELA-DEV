import cv2
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc
import scipy.ndimage
import skimage.filters
import sklearn.metrics
import random as rng
import imutils


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 3:
            shape = "triangle"
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"
        # return the name of the shape
        return shape


def testimg():
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Read image*
    image = cv2.imread("C:\\Users\\baudo\\PycharmProjects\\PAMELA-DRIVE\\helper\\importer\\drive1.bmp")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(gray.copy(), cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    i=0
    for c in cnts:
        if i != 0 :
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            cX = int((M["m10"] / M["m00"]) * 1)
            cY = int((M["m01"] / M["m00"]) * 1)
            shape = sd.detect(c)
            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image

            c = c.astype("int")
            image = cv2.drawContours(image, [c], -1, (255, 0, 0), 2)
            if shape == "rectangle" or shape == "square":
                i=i+1

                k = image[cY, cX]
                k1=image[cY, cX]

                if k[0] == 0 and k[1] == 255 and k[2]==0:
                    cv2.putText(image, "pickup", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 2)
                if k[0] == 0 and k[1] == 0 and k[2]==255:
                    cv2.putText(image, "dropoff", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 2)
                #image = cv2.rectangle(image, (cX, cY), (cX, cY), (255,0,0), 5)

                print(k)
        else :
            i = i + 1
    # show the output image
    print(i)
    cv2.imshow("Image", image)

    cv2.waitKey()
