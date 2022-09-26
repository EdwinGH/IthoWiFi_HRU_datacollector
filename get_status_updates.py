#!/usr/bin/env python
#
# Itho Daalderop HRU300 request system
# Release 2022-09-07 First version
# Release 2022-09-11 Extended set of variables, integrated CO2 sensor reading
# Release 2022-09-26 Reworked to collecting all fields to see which ones are actually updated

# RAW set of variables read on firmware "2.4.0-beta1":
# "Speed status": 0.5,
# "Internal fault": 0,
# "Frost cycle": 0,
# "Filter dirty": 0,
# "AirQuality (%)": 80,
# "AirQbased on": 1,
# "CO2level (ppm)": 0,
# "Indoorhumidity (%)": 3,
# "Outdoorhumidity (%)": 0,
# "Exhausttemp (\u00b0C)": 0,
# "SupplyTemp (\u00b0C)": 3.59,
# "IndoorTemp (\u00b0C)": 41.78,
# "OutdoorTemp (\u00b0C)": 205.57,
# "SpeedCap": 0,
# "BypassPos (%)": 22,
# "Error number": 0,
# "Status": 5,
# "Measured outside temperature (\u00b0C)": 17.15,
# "Measured temperature of mixed outside air (\u00b0C)": 14.47,
# "The flow of the inflated air (M3/h)": 404.5,
# "Inlet temperature (\u00b0C)": 20.03,
# "Temperature of the extracted air (\u00b0C)": 20.35,
# "Temperature of the blown out air of the house (\u00b0C)": 25.12,
# "The flow of the blown air (m3/h)": 307.6,
# "Relative fanspeed (%)": 0,
# "Absolute speed of the fan (%)": 4,
# "Hysteresis use in control mode (K)": 0,
# "Timer for how long the house is cooled (hour)": 0,
# "Timer for how long the house is heated (hour)": 0,
# "The mass flow of the air entering the house (kg/h)": 490.79,
# "The mass flow of the air leaving the house (kg/h)": 362.66,
# "Percentage that the bypass valve is open (%)": 74.5,
# "The desired inlet temperature (\u00b0C)": 22,
# "Hysteresis of the frost (K)": 0,
# "Number of steps the frost valve is open (steps)": 1400,
# "Number of hours of too cold air (hour)": 0,
# "Temporary speed reduction (rpm)": 0,
# "Sample timer in frost mode (min)": 0,
# "RPM of the motor (rpm)": 358,
# "Measured waste temperature heated NTC (\u00b0C)": 25.29,
# "Measured blend temperature heated NTC (\u00b0C)": 25.22,
# "Desired capacity (m3/h)": 0,
# "Busy doing adjustments (-)": 0,
# "Current consumption of fan (mA)": 434,
# "Desired current consumption of fan (mA)": 0,
# "Highest measured RH (%)": 0,
# "Highest measured CO2 (ppm)": 662

from time import sleep
from datetime import datetime
import urllib.request
import json
import operator

status_url = "http://nrg-itho/api.html?get=ithostatus"
remote_url = "http://nrg-itho/api.html?get=remotesinfo"

object_changes = {}

# First get complete status overview
req = urllib.request.Request(status_url)
# Parsing response
r = urllib.request.urlopen(req).read()
old_cont = json.loads(r.decode('utf-8'))
#print("RAW:")
#print(json.dumps(old_cont, indent=2))

for obj in old_cont:
  object_changes[obj] = 0 
print("Changes to objects:")
for key, value in object_changes.items():
  print('\t' + str(key) + "\t" + str(value))

while True:
  # First get complete status overview
  req = urllib.request.Request(status_url)
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  # Parsing response
  r = urllib.request.urlopen(req).read()
  new_cont = json.loads(r.decode('utf-8'))

  if old_cont != new_cont:
#    print("Data was changed - Collecting Changes")
    for obj in old_cont:
      if obj not in new_cont:
        print("**Key Removed**:", obj)
      else:
        if old_cont[obj] != new_cont[obj]:
          print("Key: ", obj, end='')
          print("\t was: ", old_cont[obj], end='')
          print("\t is:", new_cont[obj])
          object_changes[obj] += 1
    for obj in new_cont:
      if obj not in old_cont:
        if obj not in new_cont:
          print("**Key Added**:", obj)
          object_changes[obj] = 0

  print("Changes to objects:")
  sort_by_updates = operator.itemgetter(1)
  sorted_object_changes = sorted(object_changes.items(), key=sort_by_updates, reverse=True)
  for key, value in sorted_object_changes:
    print('\t' + str(key) + "\t" + str(value))
  old_cont = new_cont

  print("")
  # Sleep 15s before going back into eternal loop
  sleep(15)
