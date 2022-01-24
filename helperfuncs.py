import cv2 as cv
import serial

def initializeSpike(spike):
	# End serial ouput:
	spike.write(b'\x03')
	spike.write(b'\x03')
	spike.write(b'\x03')
	spike.write(b'\x03')
	spike.readlines() # clear up output
	#Initialize
	spike.write('import hub\r\n'.encode())
	spike.write('import utime\r\n'.encode())
	spike.write('motor = hub.port.A.motor\r\n'.encode())
	spike.write('motor.run_to_position(0, 50)\r\n'.encode()) # set motor to zero degrees

def detectAndDisplay(frame, face_cascade):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    
    faces = face_cascade.detectMultiScale(frame_gray) # Detect faces
    
    if len(faces) is not 0:
        x_center = faces[0][0] + (faces[0][2]) // 2 # get x-coord of 1st face center
    else:
        x_center = -1 # if no face is found, return -1

    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        
    cv.imshow('Face Detection', frame)
    return x_center