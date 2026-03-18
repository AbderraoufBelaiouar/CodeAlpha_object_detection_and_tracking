import cv2
import numpy as np
cap=cv2.VideoCapture("car-detection.mp4")
object_detector=cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=40)
while True:
    ret,frame=cap.read()
    mask=object_detector.apply(frame)
    contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # roi=
        area=cv2.contourArea(contour)
        if area>1000:
            cv2.drawContours(frame,[contour],-1,(0,255,0),2)
    cv2.imshow("frame",frame)
    cv2.imshow("mask",mask)
    key=cv2.waitKey(30)
    if key==27:
        break
cap.release()
cv2.destroyAllWindows()