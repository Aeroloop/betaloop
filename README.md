# Betaloop

Betaloop is a flight simulator with the  goal of providing accurate
and realistic flight performance primarily to be used in hardware/software in the loop testing for UAVs. This specific
implementation is for testing the
[Betaflight](https://github.com/betaflight/betaflight) flight controller in
[Gazebo](http://gazebosim.org/). 
![Betaloop](https://raw.githubusercontent.com/Aeroloop/betaloop/master/images/screenshot.png)

collection of programs and scripts with the
# Features

1. Uses real flight control firmware (Betaflight)  
2. Supports first person view (FPV) flight
3. Use your own radio controller!  

# Requirements

1. Gazebo 8 
2. [Aeroloop Gazebo resources](https://github.com/Aeroloop/aeroloop_gazebo)
2. [Betaflight](https://github.com/betaflight/betaflight) [compiled for
   SITL](https://github.com/betaflight/betaflight/tree/master/src/main/target/SITL)
3. Python3
4. [VidRecv](https://github.com/Aeroloop/vidrecv)
5. [MSP virtual radio](https://github.com/Aeroloop/msp_virtualradio) 

# Instructions
For required software part of Aeroloop make sure to follow the install
instructions specified by their respective README file.
For ease of use, add your arguments to config.txt, if needed these can be
overridden by command line arguments. 

Run the script to start the simulator,
```
python3 start.py
```

# Notes
When Betaflight is started a .bin is created and the configuration settings are
saved here. This is saved in the *current* directory. Be careful as this can
currently cause a .bin to be overwritten if testing multiple builds.

# Motor Mapping
This will be changed in the future so they match however current mappings are,

Gazebo 

Rotor 0 = Front Right
Rotor 1 = Back Left
Rotor 2 = Front Left
Rotor 3 = Back Right

Standard BF Mixer

Rotor 0 = Back Right
Rotor 1 = Front Right
Rotor 2 = Back Left
Rotor 3 = Front Left
