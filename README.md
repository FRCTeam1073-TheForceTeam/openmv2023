# openmv2023
OpenMV Vision Code for 2023 Season


# Serial Protocol

This season we will talk to our OpenMV cameras through their UART 1 / Serial Port. We plan to use 230400 bits/second, N,8,1 communications format.
Each message to and from the OpenMV camera will be a single line of text delimited by a newline character.
Within each message, fields will be separated by the comma ',' character.

## Target Message
The target message is a message from the OpenMV to the RoboRio containing a set of detected target objects.
Each detected object has four fields:

  - Type - Meaning cone or cube
  - X Image Coordinate
  - Y Image Coordinate
  - Confidence - Floating point 0 to 1 confidence in the detection
  
  
Example message:  "Cone, 100, 120, 0.5, Cube, 120, 150, 0.9, Cone, 90, 80, 1.0\n"

This represents detection of 3 game pieces. Two cones, one cube at different location and confidence levels.

