# Wiimote Algorithm

Python algorithm that uses the CWiid library to translate a Wiimote's data into a usable coordinate.

**LINUX ONLY** - CWiid is built for Linux systems, such as Debian, Ubuntu and Pi OS.

## Features

- **Wiimote Connection**: Connects to a Wiimote via Bluetooth.
- **Accelerometer Data Processing**: Reads the Wiimote's x, y, and z accelerometer data to measure tilt and roll angles.
- **Roll Angle Calculation**: Calculates the roll angle based on accelerometer data.
- **IR Tracking**: Tracks visible IR points, using these points to calculate the Wiimote's movement in space.
- **Velocity and Friction Simulation**: Smoothly interpolates between points to simulate velocity and adds friction to slow down motion over time when positioning data is lost.

## Requirements
### **Python 3**
### **CWiid**
[CWiid](https://github.com/abstrakraft/cwiid) is a Linux Nintendo wiimote interface library. It contains the following parts:
- libcwiid - Wiimote API.
- cwiid module - Python interface to libcwiid.
- wmgui - GTK gui to the Wiimote.
- wminput - An event/joystick/mouse driver for the Wiimote.
- lswm - List wiimote devices (in the spirit of ls{,pci,usb}, etc.

The original project is 15 years old as of writing, **please install from this updated fork:** https://github.com/pd-l2ork/cwiid
### **(Optional Extra) Pygame**
[Pygame](https://www.pygame.org/wiki/GettingStarted) is a library for game development and rendering. It can be installed to demonstrate the algorithm visually but is not necessary for the x and y output.

## Future Improvements:
- [ ] Allow multiple connections with separate outputs.
- [ ] Add 3D tracking via IR source triangulation, currently only tracks in a 2D space.
- [ ] Filter Accelerometer Noise, could apply a low-pass filter to smooth out accelerometer readings.
- [ ] Add Kalman Filtering to IR Data, positioning data can be jumpy in certain lighting conditions.
- [ ] Add multithreading, the program currently runs on a single thread.
