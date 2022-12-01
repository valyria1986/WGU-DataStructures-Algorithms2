#!/usr/bin/env python3
#Jared-Michael Torres
#Student ID: 000961916
#WGU-C950
#10/05/22

import csv
from Package import Package
from Truck import Truck
import datetime
import chainingHashTable

#packageDelivery.py runs in time complexity of O(n^2)

#main runs in O(n) time complexity
def main(time):

    packageHash = loadPackageData('WGUPS Package File.csv') #creates hash table of packages
    distanceData = (loadDistanceData('WGUPS Distance Table.csv'))
    packageHash.search(9).address = '410 S State St'  # corrects incorrect address of package #9
    packageHash.search(9).zipcode = '84111'
    loadAddressData('WGUPS Distance Table.csv', packageHash) #loads address data and assigns packages a location ID

    truck1 = Truck() #creates truck objects
    truck2 = Truck()
    truck3 = Truck()

    truck1.departureTime = datetime.timedelta(hours=int(8)) #assigns departure times to trucks
    truck2.departureTime = datetime.timedelta(hours=int(9), minutes=int(10))
    truck3.departureTime = datetime.timedelta(hours=int(11))

    loadTruck1(truck1, packageHash) #loads the trucks based on package constraints
    loadTruck2(truck2, packageHash)
    loadTruck3(truck3, packageHash)

    deliverPackages(truck1, packageHash, distanceData) #delivers trucks packages
    deliverPackages(truck2, packageHash, distanceData)
    deliverPackages(truck3, packageHash, distanceData)

    if time == "6":
        print(distanceData[1][18], distanceData[18][19], distanceData[1][19])

    if time == "3": #prints total miles of trucks
        print("\033[33m {}\033[00m" .format("\n Miles Traveled: "),truck1.milesTraveled + truck2.milesTraveled + truck3.milesTraveled)
    elif time == "1": #prints a list of all packages
        for items in range(0, 40):
            print(packageHash.search(items + 1))
    else:
        timeStatus(packageHash, time) #calls timeStatus function for package status list.

# loadPackageData runs in time complexity of O(n)
def loadPackageData(fileName): #loads all package data creating a package object for each and storing in hash table.
    packageHash = chainingHashTable.ChainingHashTable()
    with open(fileName) as packages:
        packageData = csv.reader(packages, delimiter = ',')
        i = 0
        while i < 5: #skips headers and empty lines
            next(packageData)
            i += 1
        for package in packageData: #loops through package list file
            pKey = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = 'At the HUB'

            #create package object
            package = Package(pKey, pAddress, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus)

            #inserts into hash table
            packageHash.insert(pKey, package)
        return packageHash


# loadDistanceDate runs in O(n^2) time complexity
def loadDistanceData(fileName): #loads all addresses and distances between each address into a 2D list
    with open(fileName) as distances:
        distanceData = csv.reader(distances, delimiter = ',')
        distanceTable = []
        i = 0
        while i < 7:  # skips headers and empty lines
            next(distanceData)
            i += 1
        for distance in distanceData:
            listDistances = distance
            listDistances.remove(listDistances[0])
            distanceTable.append(listDistances)
        for x in range(0, len(distanceTable)): #equalizes the distance table
           for y in range (0, len(distanceTable)):
                distanceTable[x][y] = distanceTable[y][x]
    return distanceTable

#loadAddressData() runs in time complexity O(n^2)
def loadAddressData(fileName, packageHash):
    with open(fileName) as address:
        addressData = csv.reader(address, delimiter = ',')
        i = 0
        while i < 7:  # skips headers and empty lines
            next(addressData)
            i += 1
        addressList = next(addressData)
        addressList.remove(addressList[0])

        for i in range(0, 40):  # Assigns the packages location index in the address list O(n^2)
            for x in range(0, len(addressList)):
                if packageHash.search(i + 1).address in addressList[x]:
                    packageHash.search(i + 1).locationID = x

# loadTruck1() runs in O(n^2) time complexity
def loadTruck1(truck, packageHash): #loads up to 16 packages with early delivery times and matching addresses unless package is delayed in flight
    count = 0
    truckPackages = []

    for items in range (0,40):
        if (packageHash.search(items+1).deliver_by != 'EOD') and (('Delayed on flight' in packageHash.search(items+1).spec_instruct) == False)\
                or packageHash.search(items+1).key == packageHash.search(19).key:
            truckPackages.append(packageHash.search(items+1))
            packageHash.search(items+1).deliveryStatus = 'En Route'
            packageHash.search(items+1).departureTime = truck.departureTime
            count += 1

    if count < 16:
        for items in range(0, 40):
            for x in range(0, len(truckPackages)):
                if (packageHash.search(items+1).deliveryStatus == 'At the HUB') and (packageHash.search(items + 1).address == truckPackages[x].address)\
                        and packageHash.search(items+1).spec_instruct == '':
                    truckPackages.append(packageHash.search(items + 1))
                    packageHash.search(items + 1).deliveryStatus = 'En Route'
                    packageHash.search(items + 1).departureTime = truck.departureTime
                    count += 1
            if count == 16:
                break
    truck.packages = truckPackages

# loadTruck2() runs in O(n^2) time complexity
def loadTruck2(truck, packageHash): #loads up to 16 packages with special delivery instructions and same addresses unless wrong address listed
    count = 0
    truckPackages = []

    for items in range (0,40):
        if (packageHash.search(items+1).deliveryStatus == 'At the HUB') and \
                (packageHash.search(items+1).spec_instruct != ''):
            truckPackages.append(packageHash.search(items+1))
            packageHash.search(items+1).deliveryStatus = 'En Route'
            packageHash.search(items + 1).departureTime = truck.departureTime
            count += 1
            if truckPackages[count-1].spec_instruct == 'Wrong address listed':
                truckPackages.remove(truckPackages[count-1])
                packageHash.search(items+1).deliveryStatus = 'At the HUB'
                packageHash.search(items + 1).departureTime = truck.departureTime
                count -= 1

    if count < 16:
        for items in range(0, 40):
            for x in range(0, len(truckPackages)):
                if (packageHash.search(items+1).deliveryStatus == 'At the HUB') and (packageHash.search(items + 1).address == truckPackages[x].address)\
                        and packageHash.search(items+1).spec_instruct == '':
                    truckPackages.append(packageHash.search(items + 1))
                    packageHash.search(items + 1).departureTime = truck.departureTime
                    packageHash.search(items + 1).deliveryStatus = 'En Route'
                    count += 1
            if count == 16:
                break

    truck.packages = truckPackages

# loadTruck() runs in O(n) time complexity
def loadTruck3(truck, packageHash): #loads up to 16 packages with no special conditions except for being 'At the HUB'
    count = 0
    truckPackages = []
    for items in range (0,40):
        if packageHash.search(items+1).deliveryStatus == 'At the HUB':
            truckPackages.append(packageHash.search(items+1))
            packageHash.search(items+1).deliveryStatus = 'En Route'
            packageHash.search(items + 1).departureTime = truck.departureTime
            count += 1
        if count == 16:
            break
    truck.packages = truckPackages

# deliverPackages() runs in O(n^2) time complexity.
def deliverPackages(truck, packageHash, distanceData): #Searches and delivers packages in truck based on nearest address.
    currentAddress = 1
    shortestDistance = 100.0
    tempAddressKey = int
    packageIndex = int
    time = truck.departureTime
    while len(truck.packages) != 0:
        for i in range (0, len(truck.packages)):
            destinationAddress = truck.packages[i].locationID
            if float(distanceData[currentAddress][destinationAddress]) <= shortestDistance:
                shortestDistance = float(distanceData[currentAddress][destinationAddress])
                destination = truck.packages[i].locationID
                tempAddressKey = truck.packages[i].key
                packageIndex = i
        currentAddress = destination
        truck.packages.remove(truck.packages[packageIndex])
        truck.milesTraveled += shortestDistance
        packageHash.search(tempAddressKey).deliveryStatus = 'Delivered'
        travelInMinutes = (shortestDistance * 60) / 18
        time += datetime.timedelta(minutes=travelInMinutes)
        packageHash.search(tempAddressKey).deliveryTime= time
        shortestDistance = 100.0
    truck.milesTraveled += float(distanceData[packageHash.search(tempAddressKey).locationID][1])

# timeStatus() runs in time complexity of O(n)
def timeStatus(packageHash: object, inputTime): #checks user input time and prints delivery status based on time
    (h, m, s) = inputTime.split(':')
    time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    for i in range(0,40):
        if time <= packageHash.search(i + 1).departureTime:
            print('Package #', packageHash.search(i + 1).key, ' address: ',
                  packageHash.search(i + 1).address, ' city: ', packageHash.search(i + 1).city,
                  ' zipcode: ', packageHash.search(i + 1).zipcode, "\033[96m {}\033[00m" .format(' Delivery Status: At HUB '))
        if packageHash.search(i + 1).deliveryTime > time > packageHash.search(i + 1).departureTime:
            print('Package #', packageHash.search(i + 1).key, ' address: ',
                  packageHash.search(i + 1).address, ' city: ', packageHash.search(i + 1).city,
                  ' zipcode: ', packageHash.search(i + 1).zipcode, "\033[93m {}\033[00m" .format(' Delivery Status: En Route '))
        if packageHash.search(i + 1).deliveryTime <= time:
            print('Package #', packageHash.search(i + 1).key, ' address: ',
                  packageHash.search(i + 1).address, ' city: ', packageHash.search(i + 1).city,
                  ' zipcode: ', packageHash.search(i + 1).zipcode,
                  "\033[92m {}\033[00m" .format(' Delivery Status: Delivered '),
                  packageHash.search(i + 1).deliveryTime)