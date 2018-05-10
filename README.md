# Betaloop

Betaloop is collection of programs and scripts with the goal to provide accurate
and realistic hardware/software in the loop testing for UAVs. This specific
implementation is for testing the
[Betaflight](https://github.com/betaflight/betaflight) flight controller in
[Gazebo](http://gazebosim.org/).

![Betaloop](https://raw.githubusercontent.com/Aeroloop/betaloop/master/images/screenshot.png)
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
