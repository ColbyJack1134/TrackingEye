# TrackingEye
Code that makes the Adafruit animated eye (https://learn.adafruit.com/animated-snake-eyes-bonnet-for-raspberry-pi) track people's position with a camera and OpenCV

The 'added pi code' contains the code that communicates with the eye and is placed on the Raspberry Pi. 'eyes.py' is a slightly modified version of the code already given by adafruit and in the /boot/Pi-Eyes/ directory. The 'custom' folder should also be placed in that directory. Finally for the pi to run the code the code in the startup folder needs to be run on startup. 

The 'server code' contains the code that would be placed on a web server powerful enough to do OpenCV proccessing relativly quickly. 'main.py' is the actual server code that communicates with the pi and processes all of the data. The 'html' folder should be placed under /var/www/html/images/ in order to get a semi-live feed of the pictures being sent by the Raspberry Pi.
