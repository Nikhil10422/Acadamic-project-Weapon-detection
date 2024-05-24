import cv2
image = cv2.imread('nikki.jpg')
cv2.imshow('original',image)
cv2.rectangle(image,(300,450),(500,600),(0,255,0),-1)
cv2.imshow('original',image)
grayscale = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow('grayscaale',grayscale)
