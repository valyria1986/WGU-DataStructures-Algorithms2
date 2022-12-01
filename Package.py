#!/usr/bin/env python3
#Jared-Michael Torres
#Student ID: 000961916
#WGU-C950
#10/05/22

#Package.py runs in time complexity of O(n)
class Package:
    def __init__(self, key, address, city, state, zipcode, deliver_by, weight, spec_instruct, deliveryStatus):
        self.key = key
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deliver_by = deliver_by
        self.weight = weight
        self.spec_instruct = spec_instruct
        self.deliveryStatus = deliveryStatus
        self.locationID = int
        self.deliveryTime = ''
        self.departureTime = ''

    def __str__(self): #overwrites print(Package) to return package information instead of object reference.
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s " %(self.key, self.address, self.city, self.state,
            self.zipcode, self.deliver_by, self.weight, self.spec_instruct, self.locationID)
