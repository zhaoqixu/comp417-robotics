IMPORTANT LICENSING NOTE:

This code has been kindly shared by researchers at McGill solely for helping you learn about robotics.
The original authors reserve all rights and provide no warranties on this code. You are only authorized
to use it for the COMP 417/765 Assignment 2 and may not not distribute, use or publish it for any other
purpose. 

Note the above is just a formality and we'd probably be happy to give you a proper licensed version
if you talk to us... in case you're interested the authors include:
Yogesh Girdhar, Anqi Xu, Florian Shkurti, Juan Camilo Gamboa Higuera, Bir-Bikram Dey, 
David Meger and Gregory Dudek.  

This is a catkin workspace that contains the localization examples and the simulator for the world.
Build with:
$ catkin_make

To run the simulator:

1) in planar mode for 417 testing:
$ roslaunch aqua_gazebo aqua.launch planar_mode:=1
2) allowing full 3D motion for 765:
$ roslaunch aqua_gazebo aqua.launch planar_mode:=0

Once the simulator is running, to make the robot move:
$ roslaunch comp417_assign2 control_helpers.launch --screen
This gives you keyboard control:
  -- First, switch the mode with 
    -- 0 -> (default) control is off so other keys will have no effect
    -- 1 -> enables angles-mode control, no depth regulation
    -- 4 -> for depth-regulated control
  -- Change the speeed:
    -- w/s -> increase/decrease forward speed
  -- Change the target angle:
    -- j/l -> yaw left and right
    -- i/k -> pitch down and up
    -- u/o -> roll left and right
  -- Hit the brakes:
    -- q