# Raspberry Pi Camera Face Detection Turret!

![PiCam1](https://user-images.githubusercontent.com/65100243/101294201-d4aacf80-37e3-11eb-9805-23a3fd5255e6.PNG)  ![PiCam2](https://user-images.githubusercontent.com/65100243/101294204-dbd1dd80-37e3-11eb-8cb5-407de8235c46.PNG)

## Overview
Welcome to my Raspberry Pi face-following project. It consists of a Pi Zero W that reads frames from the camera module, performs face detection using a Haar cascade classifier, then actuates the two servo motors to pan and tilt the camera toward the detected face. The "i2c_servo.py" file is a custom module that contains a class which inherits from a parent class in Adafruit's ServoKit library. The main purpose of this custom module is to keep all the bus, board, and servo settings separate from the main file for a little bit of cleanliness. The "CamCtrl.py" file contains the main code.

## Hardware
- Raspberry Pi Zero WH
- I2C servo driver HAT for potential future integration with other projects
- Raspberry Pi camera module
- External power supply to prevent damage to the Pi due to the noise in the servos
- Two MG90s servo motors
- 3D printed chassis (modeled in Solidworks and printed in PLA on an Ender 3 Pro)

## Software
I didn't have a spare monitor or an HDMI switch so this was all done headless in the Nano editor, through SSH. Viewing the camera's output through SSH was tricky; but was solved with X11-forwarding, ie. exporting the Pi's graphic output to an X-server on my PC (using VcXsrv).  

The following command forwards the Pi's display to my PC: `export DISPLAY=192.168.1.26:0.0`

## Demo
Due to hardware limitations in the Pi Zero, I was only able to get a workable frame rate at an abysmal resolution of 192x128. However, there are ways to slightly improve the frame rate - such as using threads to run different processes in parallel.

![CamGif](https://user-images.githubusercontent.com/65100243/101294383-e6d93d80-37e4-11eb-87ad-8511c7733dbd.gif)  ![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/65100243/101294448-564f2d00-37e5-11eb-9840-8ae5650dfc7b.gif)
