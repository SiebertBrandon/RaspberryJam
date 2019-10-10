# RaspberryJam
> LED Music Visualizer Project for the Raspberry Pi 3

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Introduction
This application is intended to run on the OSMC Raspberry Pi operating system. Why OSMC over Raspbian? OSMC is much more light-weight out of the box and provides a more stable Bluetooth protocol stack than Raspbian. During our tests, we found that streaming audio to a Raspbian operating system over Bluetooth can cause long-term instability with playback. OSMC had minimal issues while streaming.

## Setup
Before setting up everything, ensure you have a 5050 SMD LED light strip and a Raspberry Pi 3B

* Install OSMC onto the PI
* Follow through this tutorial to set up the environment and light control:
https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/
* Install Bluez
* Follow this Gist to get turn your raspberry pi into a Bluetooth audio sink:
https://gist.github.com/joergschiller/1673341
* Run lightpatternv2.py as an executable

## Update History

* 0.1.0
    * Audio streaming is functional
* 0.0.2
    * Added default light color scheme
    * Added automatic audio device detection
* 0.0.1
    * Work in progress

## Credits
Brandon Siebert [@SiebertBrandon]

Warren Seto

Olivia Shanley

## Misc
Pull requests are welcome!

Distributed under the XYZ license. See ``LICENSE`` for more information.
