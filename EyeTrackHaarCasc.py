#Face tracking
#Diego Campeao - Jan/2019

import cv2
import numpy as np
import time
import pyautogui

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Get first camera going
cap = cv2.VideoCapture(0)

mouse_pos_before = pyautogui.position()
count = 0
while True:
    #Wait 0.2s
    time.sleep(0.2)

    #Read image from camera
    ret, img = cap.read()

    out = cv2.addWeighted( img, 1.7, img, 0, 1.5)
    gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)

    #Get all faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    height, width = img.shape[:2]

    #Get image center
    center_x = width/2
    center_y = height/2

    #Size of the central rectangle in which the cursor does not move
    margin = 30

    mouse_pos = pyautogui.position()

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

        #Get face center
        face_center_x = x+w/2
        face_center_y = y+h/2

        #Distance from cursor to center of face
        d = np.sqrt((face_center_x-center_x)**2+(face_center_y-center_y)**2)

        #Step of cursor movement
        step = d - 30

        #Mouse movements. The try is here because if the mouse reaches the end of the screen an error would be raised.
        try:
            if face_center_x > center_x+margin:
                mouse_pos = pyautogui.position()
                pyautogui.moveTo(mouse_pos[0]+step, mouse_pos[1])
                print('right')
            elif face_center_x < center_x-margin:
                mouse_pos = pyautogui.position()
                pyautogui.moveTo(mouse_pos[0]-step, mouse_pos[1])
                print('left')
            if face_center_y > center_y+margin:
                mouse_pos = pyautogui.position()
                pyautogui.moveTo(mouse_pos[0], mouse_pos[1]+step)
                print('down')
            elif face_center_y < center_y-margin:
                mouse_pos = pyautogui.position()
                pyautogui.moveTo(mouse_pos[0], mouse_pos[1]-step)
                print('up')
        except:
            pass

    #Mouse is in the same position as in previous step?
    if mouse_pos == mouse_pos_before:
        count += 1
    else:
        count = 0

    #If cursor stays in the same place for 10 cycles (2 seconds) then click
    if count > 10:
        pyautogui.click()
        count = 0

    mouse_pos_before = mouse_pos

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
