from djitellopy import tello
import time
import cv2
import keyboard
global img
def getKeyboardInput():
    #LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 80 
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100
    if keyboard.is_pressed('left'):
        lr = -speed
    if keyboard.is_pressed('right'):
        lr = speed
    if keyboard.is_pressed('up'):
        fb = moveSpeed
    if keyboard.is_pressed('down'):
        fb = -moveSpeed
    if keyboard.is_pressed('w'):
        ud = liftSpeed
    if keyboard.is_pressed('s'):
        ud = -liftSpeed
    if keyboard.is_pressed('d'):
        yv = rotationSpeed
    if keyboard.is_pressed('a'):
        yv = -rotationSpeed
    if keyboard.is_pressed('q'):
        Drone.land()
        time.sleep(3)
    if keyboard.is_pressed('e'):
        Drone.takeoff()
    if keyboard.is_pressed('z'):
        cv2.imwrite(f"Drone/Images/{time.time()}.jpg", img)
        time.sleep(0.3)
    return [lr, fb, ud, yv]
Drone = tello.Tello()
Drone.connect()
print(Drone.get_battery())
Drone.streamon()
while True:
    keyValues = getKeyboardInput()
    Drone.send_rc_control(keyValues[0], keyValues[1], keyValues[2], keyValues[3])
    img = Drone.get_frame_read().frame
    img = cv2.resize(img, (1080, 720))
    cv2.imshow("DroneCapture", img)
    cv2.waitKey(1)
