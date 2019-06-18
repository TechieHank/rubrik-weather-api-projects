# Rubrik Weather API Python Script - Version 1.0.0
# By: Enrique Barreto
# Last Modified: June 2019

# Instructions
# This scripts uses Rubrik SDK module for Python (https://build.rubrik.com/sdks/python/) as well as OpenWeatherMap.org SDK module (called pyowm - https://pyowm.readthedocs.io/en/latest/)
# The script looks for coordinates (latitude and longitude) of a map, checks for a meteorological event in those coordinates and if it finds a specific number is greater or lower
# than reading from OperWeatherMap, it executes a command within Rubrik. That command can be ANYTHING - in this case, we are running an ON-DEMAND backup of several virtual machines
# associated with a SLA policy called "Gold"

import pyowm
import rubrik_cdm
import urllib3
from datetime import datetime, timedelta

# Disable certificate warnings and connect to Rubrik Cluster
urllib3.disable_warnings()

# Provide OWM API Key to make weather calls - this is your personal
owm = pyowm.OWM('your openweathermap API key')

# Give me all the weather forecast for the next 3 hours at the following coordinates
data = owm.three_hours_forecast_at_coords(38.9403,-74.9387)

# Create a definition class
def activate():

# Set variables for Rubrik cluster in Gaia Lab - Note: you can set these variables on your BASH shell (Don't need to hardcode here)
    node_ip = "rubrik IP address"
    username = "rubrik username"
    password = "rubrik password"

# Establish a connection to the Rubrik cluster
    rubrik = rubrik_cdm.Connect(node_ip, username, password)
    print ("Establishing Connection with Rubrik Cluster...")

# Set Rubrik Object Variables
    sla = "name of SLA policy"
    object_type = "rubrik object being protected - example: vmware"
    all_vms_in_sla = rubrik.get_sla_objects(sla, object_type)

# Take On-Demand Snapshot of all VM's in a SLA
    for vm_name, _ in all_vms_in_sla.items():
        rubrik.on_demand_snapshot(vm_name, object_type, sla)

# Manipulate DATE and TIME to get advanced forecast. We will call OpenWeatherMap API to tell us what the speed is going to be for the latitude and longitude for the next THREE HOURS of a 24 Hour Forecast
h = 0
while h <= 24:
    time = datetime.now() + timedelta(days=1, hours = h)
    now = data.get_weather_at(time)
    speed = now.get_wind()['speed']
    print ("Forecasted wind speeds in " + str(h) + " hours will be " + str(speed) + " Miles per Hour")

# What happens if the wind speeds are greater than a certain threshold.If speed condition is met, run the ACTIVATE definition class and BREAK the clause to EXIT 
    if speed >= 5.000:
        print ("THE HURRICANE IS COMING!!!!! - RUN ON-DEMAND BACKUP")
        activate()
        break
    h += 3

# End of Script
