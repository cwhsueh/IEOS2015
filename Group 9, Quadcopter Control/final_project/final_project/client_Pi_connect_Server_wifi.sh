#!/bin/bash

su
iwconfig wlan0 essid RPi-AP
dhclien wlan0
dhclien -r wlan0
dhclien wlan0
ifconfig
