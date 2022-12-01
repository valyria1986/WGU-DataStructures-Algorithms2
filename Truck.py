#!/usr/bin/env python3
#Jared-Michael Torres
#Student ID: 000961916
#WGU-C950
#10/05/22

#Truck.py runs in time complexity of O(n)
class Truck:
    def __init__(self):

        self.packages = []
        self.departureTime = ''
        self.milesTraveled = 0.0
    def __int__(self): #overwrites print(Truck) to return package information instead of object reference.
        return self.packages

