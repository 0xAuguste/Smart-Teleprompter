import time
from helperfuncs import *
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS

setpoint = 320
Kp = 0.12
Ki = 0.01
error = 0
i_error = 0

# Setup serial connection to Spike
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
initializeSpike(ser)

# Load the cascade data:
face_cascade = cv.CascadeClassifier()
if not face_cascade.load('haarcascades/haarcascade_frontalface_alt.xml'): #load face recognition file
    print('--(!)Error loading face cascade')
    exit(0)

# Start video stream:
cap = WebcamVideoStream(src=0).start() # 0 means camera live view

# MAIN LOOP:
try:
    while True:
        # Find faces
        frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        face_center = detectAndDisplay(frame, face_cascade) # x-coord of face center
        if cv.waitKey(10) == 27:
            break

        # Controller
        if face_center != -1:
            error = face_center - setpoint # proportional error
            i_error = i_error + error # integral error

            pwm_out = int(Kp * error + Ki * i_error)

            if -12 < pwm_out < 12:
                pwm_out = 0
            else:
                pwm_out = min(pwm_out, 20)
                pwm_out = max(pwm_out, -20)

            ser.write(('motor.pwm(' + str(pwm_out) + ')\r\n').encode())
        else:
            ser.write('motor.pwm(0)\r\n'.encode()) # if you can't find face, stay still

except KeyboardInterrupt:
    ser.write('motor.pwm(0))\r\n'.encode())
    ser.write('motor.run_to_position(0, 20)\r\n'.encode())
    cv.destroyAllWindows()
    cap.stop()

