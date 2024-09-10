For the HELLCOOL RERF-021 presenter, it sends commands to terminal based on the button pressed, which are then used for controlling the Franka robot for demo collection. It creates a node in ROS2 for that.

Make sure `python-evdev` package is installed:
```
pip3 install --upgrade pip 
pip install evdev
```
For the devices to be able to be read out:
```
sudo usermod -a -G input $USER
```
Reboot to apply change.
