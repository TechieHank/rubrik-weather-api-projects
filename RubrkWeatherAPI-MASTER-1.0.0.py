# Rubrik Weather API Python Script - Version 1.0.0
# By: Enrique Barreto
# Last Modified: May 2019

# Instructions
# This scripts uses Rubrik SDK module for Python (https://build.rubrik.com/sdks/python/) as well as OpenWeatherMap.org SDK module (called pyowm - https://pyowm.readthedocs.io/en/latest/)
# The script looks for coordinates (lattitude and longitude) of a map, checks for a meteorological event in those coordinates and if it finds a specific number is greater or lower
# than reading from OperWeatherMap, it executes a command within Rubrik. That command can be ANYTHING - in this case, we are running an ON-DEMAND backup of a virtual machine

import pyowm
import rubrik_cdm
import urllib3
from datetime import datetime, timedelta

# Disable certificate warnings and connect to Rubrik Cluster
urllib3.disable_warnings()

# Provide OWM API Key to make weather calls - this is your personal
owm = pyowm.OWM('yourownopenweathermapapikey')

# Give me all the weather forecast for the next 3 hours at the following coordinates
data = owm.three_hours_forecast_at_coords(-22.57, -43.12)

# Create a definition class
def activate():

# Set variables for Rubrik cluster in Gaia Lab - Note: you can set these variables on your BASH shell (Don't need to hardcode here)
    node_ip = "127.0.0.1"
    username = "your.username@yourdomain.com"
    password = "YourPassword"

# Establish a connection to the Rubrik cluster
    rubrik = rubrik_cdm.Connect(node_ip, username, password)
    print ("Establishing Connection with Rubrik Cluster...")

# Set Rubrik Object Variables
    vm_name = "yourvirtualmachinename"
    object_type = "vmware"

# Take On-Demand Snapshot of VM
    snapshot = rubrik.on_demand_snapshot(vm_name, object_type)

# Manipulate DATE and TIME to get advanced forecast. We will call OpenWeatherMap API to tell us what the speed is going to be for the latitude and longitude for the next THREE HOURS of a 24 Hour Forecast
h = 0
while h <= 24:
    time = datetime.now() + timedelta(days=1, hours = h)
    now = data.get_weather_at(time)
    speed = now.get_wind()['speed']
    print ("Forecasted Winds in the next " + str(h) + " hours will be " + str(speed) + " Miles per Hour")
    
# What happens if the wind speeds are greater than a certain threshold    
    if speed >= 2.0000:
    	print ("THE HURRICAINE IS COMING!!!!! - RUN ON-DEMAND BACKUP")
        # activate()
    h += 3
