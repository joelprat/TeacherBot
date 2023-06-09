# TeacherBot

# Table of Contents
  * [What is this?](#what-is-this)
  * [Physical Robot](#physical-robot)
  * [Hardware Scheme](#hardware-scheme)
  * [Software Scheme](#software-scheme)
  * [Requirements](#requirements)
  * [How to use](#how-to-use)
  * [TeacherBot DEMO](#teacherbot-demo)
  * [Authors](#authors)

# What is this?

This project consists of the design and construction of a robot capable of helping you to improve your knowledge of Catalan. It is able to understand and highlight syntax errors. 

It uses different electronic components, such as an Arduino board, stepper motors, motor controllers, a Bluetooth module and a servo motor. In addition, it uses the microphone and speaker of a mobile device to generate a human-robot interaction that provides a more dynamic experience. The physical implementation of the robot includes a metal structure and a robotic arm. 

This Catalan teaching robot is a great tool for anyone who wants to improve their Catalan language skills, whether to learn the language for academic or professional purposes, or just for fun. It is easy to use and very effective, which means that you will be able to significantly improve your level of Catalan in a very short time.

# Physical Robot
![image](https://github.com/joelprat/TeacherBot/blob/main/Physical%20robot.jpeg)

![image](https://github.com/joelprat/TeacherBot/blob/main/ComponentsImg.jpg)

# Hardware Scheme
![image](https://github.com/joelprat/TeacherBot/blob/main/HardwareSchema.jpg)

# Software Scheme
![image](https://github.com/joelprat/TeacherBot/blob/main/SoftwareSchema.jpg)

# Requirements

Python
 - [Python 3.11.x](https://www.python.org/)
 - [NumPy](https://numpy.org/)
 - [Sympy](https://www.sympy.org/)
 - [sympy.physics.mechanics](https://docs.sympy.org/latest/modules/physics/mechanics/index.html)
 - [requests](https://pypi.org/project/requests/)
 - [easyOCR](https://pypi.org/project/easyocr/)
 - [cv2](https://pypi.org/project/opencv-python/)
 - [socket](https://docs.python.org/3/library/socket.html)
 - [base64](https://docs.python.org/es/3/library/base64.html)
 - [translate](https://pypi.org/project/translate/)
 - [gTTs](https://pypi.org/project/gTTS/)
 - [pillow](https://pypi.org/project/Pillow/)
 - [faker](https://pypi.org/project/Faker/0.7.4/)


[Android Studio JDK](https://developer.android.com/studio):
 - SDK min 24 target 33
 - Java version 1.8
 - Java Bluetooth API
 - Java Socket API
 - Android Text To Speach
 - Android Camera API


[Arduino](https://support.arduino.cc/hc/en-us/articles/360019833020-Download-and-install-Arduino-IDE):
 - Accel Stepper version 1.64 (to be installed in arduino IDE)
 - Software Serial ((included in arduino IDE))
 - Servo.h (included in arduino IDE)
 - String.h (included in arduino IDE)


# How to use

1. Install Python.

2. Clone this repo.

    ```
    $ git clone https://github.com/joelprat/TeacherBot.git
    ```
    
3. Install the required libraries.

   If using Windows:
   
     ```
     $ cd \TeacherBot\algorithms\OCR\
     $ install_dependencies_windows.bat
     ```
     
   If using bash:
   
    ```
    $ cd /TeacherBot/algorithms/OCR/
    $ chmod +x install_dependencies_bash.sh
    $ ./install_dependencies_bash.sh
    ```

4.  Server execution.

    ```
    $ python server.py
    ```

# TeacherBot DEMO

[![Alt text](https://img.youtube.com/vi/jaYQ3ElwnmU/0.jpg)](https://www.youtube.com/watch?v=jaYQ3ElwnmU)

# Authors

- [Contributors](https://github.com/joelprat/TeacherBot/graphs/contributors)
