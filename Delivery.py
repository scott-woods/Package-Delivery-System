from datetime import datetime, timedelta

import ReadFiles

allPackages = []
loadedPackages = []
deliveredPackages = []


class Package:

    def __init__(self, packageID, address, city, state, postalCode, deadline, weight, notes, status="AT_HUB"):
        self.packageID = packageID
        self.location = None
        self.address = address
        self.city = city
        self.state = state
        self.postalCode = postalCode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.deliveryTime = None
        self.startTime = None

    # Give the Package a Location once the imported Addresses and Distance Arrays are combined into Location Objects
    def updateLocation(self):
        for location in ReadFiles.allLocations:
            if location.address == self.address:
                self.location = location

    def updateDeliveryTime(self, deliveryTime):
        self.deliveryTime = deliveryTime

    def updateStartTime(self, startTime):
        self.startTime = startTime

    # Returns a formatted String of the Package's Information, changes status based on Time vs. Delivery Time
    # Runs in O(1)
    def getAllInfo(self, inputTime):
        allInfo = None
        if self.deliveryTime > inputTime > self.startTime:
            allInfo = ("Package ID: {}, Address: {}, City: {}, "
                       "State: {}, ZIP: {}, Deadline: {}, "
                       "Weight: {}, Notes: {}, Status: ON_ROUTE, Estimated Delivery Time: {}".format(self.packageID,
                                                                                                     self.address,
                                                                                                     self.city,
                                                                                                     self.state,
                                                                                                     self.postalCode,
                                                                                                     self.deadline,
                                                                                                     self.weight,
                                                                                                     self.notes,
                                                                                                     self.deliveryTime))
        elif self.deliveryTime <= inputTime:
            allInfo = ("Package ID: {}, Address: {}, City: {}, "
                       "State: {}, ZIP: {}, Deadline: {}, "
                       "Weight: {}, Notes: {}, Status: DELIVERED, Delivery Time: {}".format(self.packageID,
                                                                                            self.address,
                                                                                            self.city, self.state,
                                                                                            self.postalCode,
                                                                                            self.deadline,
                                                                                            self.weight,
                                                                                            self.notes,
                                                                                            self.deliveryTime))
        elif inputTime < self.startTime:
            allInfo = ("Package ID: {}, Address: {}, City: {}, "
                       "State: {}, ZIP: {}, Deadline: {}, "
                       "Weight: {}, Notes: {}, Status: AT_HUB, Estimated Delivery Time: {}".format(self.packageID,
                                                                                                   self.address,
                                                                                                   self.city,
                                                                                                   self.state,
                                                                                                   self.postalCode,
                                                                                                   self.deadline,
                                                                                                   self.weight,
                                                                                                   self.notes,
                                                                                                   self.deliveryTime))
        return allInfo


class Location:

    def __init__(self, locationID, name, address, distanceArray=None):
        if distanceArray is None:
            distanceArray = []
        self.locationID = locationID
        self.name = name
        self.address = address
        self.distanceArray = distanceArray

    # Takes a Location as an argument and returns its Distance to the current Location
    def getDistance(self, location):
        targetLocation = int(location.locationID)
        if self.distanceArray[targetLocation] != '':
            return self.distanceArray[targetLocation]
        elif location.distanceArray[int(self.locationID)] != '':
            return location.distanceArray[int(self.locationID)]

    def updateDistanceArray(self, distanceArray):
        self.distanceArray = distanceArray


class Truck:

    def __init__(self, location, name, milesTraveled=0.0, speed=18, capacity=16,
                 currentTime=datetime.today().replace(hour=8, minute=0, second=0, microsecond=0)):
        self.packages = []
        self.priorityPackages = []
        self.locationsOnRoute = []
        self.location = location
        self.name = name
        self.milesTraveled = milesTraveled
        self.speed = speed
        self.capacity = capacity
        self.currentTime = currentTime

    def updateTime(self, timeInput):
        self.currentTime = timeInput

    # Takes a Package as an argument and adds it to the Truck's array of Packages
    def addPackage(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            self.locationsOnRoute.append(package.location)
            if package.deadline != "EOD":
                self.priorityPackages.append(package)
            return True
        else:
            print("The Truck is at Capacity.")
            return False

    # Moves the Truck to the Location of the next Package and Delivers it, adds Travel Time
    def dropoffPackage(self, package, distance, nextLocation):
        global deliveredPackages
        deliveredPackages.append(package)
        self.packages.remove(package)
        if package in self.priorityPackages:
            self.priorityPackages.remove(package)
        travelTime = distance / self.speed
        self.currentTime = self.currentTime + timedelta(hours=travelTime)
        self.location = nextLocation
        self.milesTraveled += distance
        package.status = "DELIVERED"
        package.updateDeliveryTime(self.currentTime)

    # Returns the Distance between the Truck's Location and another Location
    def getNextDistance(self, location):
        targetLocation = location.locationID
        if self.location.distanceArray[targetLocation] != '':
            return self.location.distanceArray[targetLocation]
        elif location.distanceArray[self.location.locationID] != '':
            return self.location.distanceArray[targetLocation]

    # Determines distance back to Hub and has the Truck travel back to the Hub, updating Time and Total Miles Traveled
    def returnHome(self, distance):
        travelTime = distance / self.speed
        self.currentTime = self.currentTime + timedelta(hours=travelTime)
        self.location = ReadFiles.allLocations[0]
        print("{} returned to Hub at: {}\n".format(self.name, self.currentTime))
        return self.currentTime
