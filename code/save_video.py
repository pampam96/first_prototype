#!/usr/bin/env python3

import cv2

cap = cv2.VideoCapture(6)

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter('green.avi', fourcc, 20,(frame_width,frame_height),True )
print(int(cap.get(3)))
print(int(cap.get(4)))

while(cap.isOpened()):
    ret,frame = cap.read()
    if ret == True:
        #print(frame.shape)
        out.write(frame)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
out.release()

cv2.destroyAllWindows()