# Rig-controller
Control a rig for manual testing of sensors

The controller is made up of four degrees of freedom. An x, y, z and tilt axis. We can use this platform to gather a series of directions, pressures, textures and angles to gather a robust dataset. This repository will provide the control for this rig so others can replicate the rig and generate their own data sets.

<img width="25%" src="https://raw.githubusercontent.com/shepai/Rig-controller/main/Assets/rig.jpeg">

The x axis is the plate moving back and fourth. The y axis moves the main body left and right. The z axis moves the sensor up and down, and the a axis tilts the plate.

We make use of a force matrix sensor such as the ones developed in the <a href="https://github.com/shepai/TactileSensor">tactile sensor repository</a> that is placed on top of the plate. This allows us to measure the force applied on the base to give extra labelling data that can be automatically gathered. 

## Set up
The Rig is controlled by a Raspberry Pi Pico. It uses I2C to connect to two Adafruit stepper motor controllers. One of the addresss (the board that controls axis z) must be soldered over to avoid desturbing the default pin address of the first board.

## Controlling the Rig
