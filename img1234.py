import cv2
image = cv2.imread("weapon.jpg")
cv2.imshow('original',image)
cv2.rectangle(image,(500,200),(990,500),(0,255,0),1)
cv2.putText(image,"weapon is detected",(600,195),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
cv2.imshow('original',image)
