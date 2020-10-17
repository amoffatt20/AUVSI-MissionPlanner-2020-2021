# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 19:19:12 2018

@author: amrey
"""

import interop

client = interop.Client(url='http://10.10.130.10:80', username='pomona', password='9499796437')
# Grab mission details and save them to text file in Documents
missions = client.get_missions()

missionpath = 'C:/Users/Public/Downloads/InteropCode/interop/Missions.txt'
missions_file = open(missionpath, 'w')
missions_file.write("\n".join(map(lambda x: str(x), missions)) + "\n")
missions_file.close()

# Grab stationary and moving obstacle details and save them to text file in Documents
stationary_obstacles, moving_obstacles = client.get_obstacles()
stationarypath = 'C:/Users/Public/Downloads/InteropCode/interop/Stationary.txt'
stationary_file = open(stationarypath, 'w')
stationary_file.write("\n".join(map(lambda x: str(x), stationary_obstacles)) + "\n")
stationary_file.close()