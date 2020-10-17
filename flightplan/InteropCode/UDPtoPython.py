# -*- coding: utf-8 -*-
"""
Created on Thr Jun  14

@author: DBannowsky
"""

import socket
import os

host = "10.0.65.1"
port = 8089
buf = 1024
addr = (host, port)

address = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = input("Enter message to send here: ")
    UDPSock.sendto(data.encode(),addr)
    if data == "exit":
        break

UDPSock.close()
os._exit(0)