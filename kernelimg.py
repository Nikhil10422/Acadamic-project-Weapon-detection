import cv2

import numpy as np

image = cv2.imread('weapon.jpg')
#Creating kernel
kernel = np.ones((7,7), np.uint8)
#Using cv2.erode()method
image = cv2.erode(image,kernel)
#Displaying the image
cv2.imshow('Erode',image)
cv2.waitKey(0)
