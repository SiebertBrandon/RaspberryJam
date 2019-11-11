# RaspberryJam
> LED Music Visualizer Project for the Raspberry Pi 3

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Introduction
RaspberryJam utilizes the [ws281x library](https://github.com/jgarff/rpi_ws281x) and an A2DP BlueZ Bluetooth audio sink to drive LED light shows.

## Required Hardware
* Raspberry Pi 3 or later
* A computer with an MicroSD card reader
* A MicroSD card with at least 16GB space
* ws281X Individually Addressable LED Light Strip (Up to a theoretical maximum of ~5000 LEDs)
* A Cellphone or Other Bluetooth Streaming Device

## Implementation
This application is intended to run on the OSMC Raspberry Pi operating system. Why OSMC over Raspbian? OSMC is much more light-weight out of the box and provides a more stable Bluetooth protocol stack than Raspbian. During our tests, we found that streaming audio to a Raspbian operating system over Bluetooth can cause long-term instability with playback. OSMC had minimal issues while streaming.

## ToDo
This repo is currently under construction. Please check back later for a release


## Setup
1. Download the OSMC image
1. Flash the OSMC image onto the MicroSD card
1. Place the MicroSD card into the Raspberry Pi and boot
1. Once booted, switch to virtual terminal using the `CTRL+ALT+F1` key combination
1. Login using the credentials Username: `osmc`, Password: `osmc`
1. Run these commands to upate
```
sudo apt update
sudo apt-get dist-upgrade
sudo apt-get clean
```
(Instructions to turn off GUI on boot)
1. Download the latest installation script from github:
```
wget some-raspberryjam-release-script
```
1. Run the installation script
1. Set some default light pattern file
1. Reboot the Raspberry Pi
1. Scan and connect using the Bluetooth Streaming Device
1. Play audio from an app like Spotify
1. Watch in awe!

New instructions coming soon
#* Install OSMC onto the PI

#* Follow through this tutorial to set up the environment and light control:

#https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

#* Install Bluez

#* Follow this Gist to get turn your raspberry pi into a Bluetooth audio sink:

#https://gist.github.com/joergschiller/1673341

#* Run lightpatternv2.py as an executable


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

Warren Seto [@nextbytes]

Olivia Shanley

## Misc
Pull requests are welcome!

Distributed under the XYZ license. See ``LICENSE`` for more information.
