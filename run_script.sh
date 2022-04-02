#!/bin/bash

# IF SCREEN RUNNING CLOSE IT
screen -XS live quit

# THIS RUN SCREE SESSION WITH NAME live
screen -dmS live /usr/bin/python3 /home/pi/Documents/serialtcp/reader.py dev


# ==================================================================================
# INSTALATION 
# sudo apt install screen

# set your reader.py full path   |--------------------------------------|
# !!! REMOVE 'dev' from end of this line !!!

# CRONTAB
# 
# crontab -e
#
# add this line at the end (without # sign)
#
# @reboot sleep 30 && bash -c "/home/pi/Documents/serialtcp/run_script.sh > /home/pi/script.log 2>&1"
#
# change run_script.sh path    |-----------------------------------------|
# 
#
#
# CHECK IF IT IS RUNNING
# 
# list screen sessions
#
# screen -ls
# 
# output shuld be like this:
#
# pi@raspberrypi:~ $ screen -ls
# There is a screen on:
#        635.live        (02/04/22 20:07:53)     (Detached)
# 1 Socket in /run/screen/S-pi.
#
#
# CONNECT TO SCREEN SESSION
# 
# screen -r live
# 
#
# EXIT FROM SCREEN SESSION
# !!!!!!!!!!!!!!!!!!!!!!!!
# !!! press: ctrl + a + d
# !!!!!!!!!!!!!!!!!!!!!!!!
#
# if you will use ctrl + c or ctrl + z, screen will close




