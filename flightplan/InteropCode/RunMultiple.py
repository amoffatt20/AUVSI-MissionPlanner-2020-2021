# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 19:20:26 2018

@author: amrey
"""

import sys
sys.path.insert(0, 'C:/Users/Public/Downloads/InteropCode/interop')
import interop

client = interop.Client(url='http://10.10.130.10:80', username='pomona', password='9499796437')

#Grab mission details and save them to text file in Documents
missions = client.get_missions()

stationary_obstacles, moving_obstacles = client.get_obstacles()
movingpath = 'C:/Users/Public/Downloads/InteropCode/interop/Moving.txt'
moving_file = open(movingpath,'w')
moving_file.write("\n".join(map(lambda x: str(x),moving_obstacles)) + "\n")
moving_file.close()
