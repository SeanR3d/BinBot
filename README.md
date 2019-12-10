# BinBot

![](res/BinBot_logo3.png)        

Temple University Computer Science Capstone Project team:

[Sean Digirolamo](https://github.com/s-digiro)    
[Sean Reddington](https://github.com/SeanR3d)    
[Michael Savitski](https://github.com/MikeSavitski)    
[Jose Silva](https://github.com/tuf06643)    
[Kwamina Thompson](https://github.com/kiloz14)    

BinBot is an autonomous robot designed to identify and collect littered waste. The robot is built from a Raspberry Pi robot kit, which includes a camera, proximity sensor, motorized treads, and a mechanical arm. This robot is powered by an embedded Raspberry Pi 3 B+. BinBot’s on-board camera captures live-feed images which are sent to a processing server. To outsource the heavy data processing from the on-site robot; this Linux server will process the images sent by BinBot using data representations created from a trained machine learning model. Using TensorFlow and OpenCV libraries, the machine learning model will identify any pieces of waste in the image. The server will then compute properties about the waste, including the location from the robot, and generate instructions for the robot to navigate to the waste and collect it. The application will also display of the images from the processing the Pi camera, which include bounding boxes surrounding any waste identified via the machine learning model. BinBot also features an Android mobile app which provides the ability to start and stop BinBot’s waste collection process.

#### Features:
- Search for, identify, navigate to, and pick up waste
- LED lights on side of robot indicate current state
	- Blue: Capturing picture, sending and receiving to server
	- Red: Executing movement instructions from server
	- Yellow: Executing patrol instructions
	- Green: Retrieving waste
- Mobile app to toggle operation of robot
- Server displays individual pictures received from BinBot

#### Bugs:
- Yes

## Modules

### BinBot Robot

This is the code for that actual robot that connects to the server, navigates to waste, and retrieves it. It runs directly on a Raspbian OS on a Raspberry PI 3 B+. It is written in Python.

##### Build instructions

The BinBot Robot does not have build instructions because it is written in Python, which is interpreted rather than compiled. But, ensure that it is downloaded onto the raspberry Pi/Robot rather than the server or anywhere else.

##### Running

To run, execute main.py with the IP address of the server configured in the file. By default, the connection is on port 7001:

`$ sudo python3 main.py`


### BinBot Processing Server

This is the server which the BinBot Robot connects to. Images are sent from the BinBot Robot to the server, and the server returns instructions to BinBot on how it should proceed in order to locate and retrieve waste. It runs on Windows and is written in Java.

##### Build instructions

Build using Javac compiler, JDK version 11.

##### Running

Ensure that OpenCV is installed on the system and that the appropriate DLL for your system is in your PATH environment variable.

Run the jar with java 11, as such:

`<path to java11> -jar <path to jar>`

### BinBot Mobile Application

Runs on Android

##### Build instructions
                            
Build using Android studio compiler, SDK version 29 , minSDKversion 23, targetSDKversion 29

##### Running

IP address needs to be identical to all the host servers IP, to allow communication.
