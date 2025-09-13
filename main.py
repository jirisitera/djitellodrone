from djitellopy import tello
import cv2
import pygame
import numpy as np
import time
import os
import sys
FPS = 60
os.environ["SDL_VIDEO_ALLOW_SCREENSAVER"] = "1"
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"
if __name__ == "__main__":
    Drone = tello.Tello()
    Drone.connect()
    program = app()
    program.init()
    program.run()
class joystick_handler(object):
    def __init__(self, id):
        self.id = id
        self.name = self.joy.get_name()
        self.joy = pygame.joystick.Joystick(id)
        self.joy.init()
        # axis
        self.numaxes = self.joy.get_numaxes()
        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))
        # buttons
        self.numbuttons = self.joy.get_numbuttons()
        self.button = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))
        # hats
        self.numhats = self.joy.get_numhats()
        self.hat = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))
class app(object):
    def init(self):
        pygame.init()
        pygame.display.set_caption("Wireless Drone Controller")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)
        pygame.event.set_blocked((pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN))
        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("This program only works with at least one joystick plugged in. No joysticks were detected.")
            self.quit(1)
        self.joy = []
        for i in range(self.joycount):
            self.joy.append(joystick_handler(i))
    def run(self):
        lr, fb, ud, yv = 0, 0, 0, 0
        Drone.streamoff()
        Drone.streamon()   
        while True:
            frame_read = Drone.get_frame_read()
            if frame_read.stopped: break
            self.screen.fill([0, 0, 0])
            frame = frame_read.frame
            text = "Battery: {}% | Max Temp: {}C".format(Drone.get_battery(), Drone.get_highest_temperature())
            cv2.putText(frame, text, (5, 720 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()
            time.sleep(1 / FPS)
            speed = 80 
            liftSpeed = 40
            moveSpeed = 90
            rotationSpeed = 100
            for event in [pygame.event.wait()] + pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.JOYAXISMOTION:
                    self.joy[event.joy].axis[event.axis] = event.value
                    if event.axis == 0:
                        lr = int(event.value * speed)
                    elif event.axis == 1:
                        fb = -int(event.value * moveSpeed)
                    elif event.axis == 2:
                        yv = int(event.value * rotationSpeed)
                    elif event.axis == 3:
                        ud = -int(event.value * liftSpeed)
                elif event.type == pygame.JOYHATMOTION:
                    self.joy[event.joy].hat[event.hat] = event.value
                    x = event.value[0]
                    y = event.value[1]
                    if x == 0 & y == 1:
                        Drone.flip_forward()
                    elif x == 0 & y == -1:
                        Drone.flip_back()
                    elif x == 1 & y == 0:
                        Drone.flip_right()
                    elif x == -1 & y == 0:
                        Drone.flip_left()


                elif event.type == pygame.JOYBUTTONDOWN:
                    self.joy[event.joy].button[event.button] = 1
                    if event.button == 0:
                        Drone.land()
                    if event.button == 3:
                        Drone.takeoff()
            Drone.send_rc_control(lr, fb, ud, yv)
    def quit(self, status=0):
        pygame.quit()
        sys.exit(status)
