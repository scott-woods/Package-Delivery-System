import csv
import HashTable
from Delivery import Truck, Package, Location, allPackages, loadedPackages

packageTable = HashTable.PackageHashTable()
allLocations = []
allDistances = []
allAddresses = []
totalMilesTraveled = 0.0

# Opens the WGUPS Addresses file, creates a Location for each address
# Runs in O(N)
with open("WGUPS Addresses.csv", "r") as addressFile:
    csv_reader = csv.reader(addressFile)
    for line in csv_reader:
        allAddresses.append(line)
        locationID = line[0]
        name = line[1]
        address = line[2]
        location = Location(locationID, name, address)
        allLocations.append(location)

# Opens WGUPS Distance Table file, adds the appropriate Distance array to each previously created Location
# Runs in O(N)
with open("WGUPS Distance Table.csv", "r") as distanceFile:
    csv_reader = csv.reader(distanceFile)
    for line in csv_reader:
        allDistances.append(line)
    for location in allLocations:
        locID = int(location.locationID)
        location.updateDistanceArray(allDistances[locID])

# Opens WGUPS Package File, creates a Package for each line in the file
# Runs in O(N)
with open("WGUPS Package File.csv", "r") as packageFile:
    csv_reader = csv.reader(packageFile)
    for line in csv_reader:
        packageID = line[0]
        address = line[1]
        city = line[2]
        state = line[3]
        postalCode = line[4]
        deadline = line[5]
        weight = line[6]
        notes = line[7]

        # Create a Package object with data from CSV file
        package = Package(packageID, address, city, state, postalCode, deadline, weight, notes)

        # Change Package with wrong address to the Correct Address
        if package.notes.__contains__("Wrong address listed"):
            package.address = "410 S State St"
            package.postalCode = "84111"

        # Give the Package a Location, insert PackageID as Key and Package as Value into the Hash Table
        package.updateLocation()
        allPackages.append(package)
        key = packageID
        value = package
        packageTable.insert(key, value)


# Creates and loads Trucks with Packages based on Restrictions
def loadTrucks():
    truck1 = Truck(allLocations[0], "Truck 1")
    truck2 = Truck(allLocations[0], "Truck 2")
    truck3 = Truck(allLocations[0], "Truck 3")
    # First, all Packages with Restrictions are loaded into their appropriate Trucks
    for package in allPackages:
        if package.notes == "Can only be on truck 2":
            truck2.addPackage(package)
            loadedPackages.append(package)
        elif package.notes.__contains__("Delayed"):
            truck3.addPackage(package)
            loadedPackages.append(package)
        elif package.notes.__contains__("Wrong address listed"):
            truck3.addPackage(package)
            loadedPackages.append(package)
        elif package.notes.__contains__("Must"):
            truck1.addPackage(package)
            loadedPackages.append(package)
    # Second, Packages with a Deadline are loaded into either Truck 1 or Truck 2
    for package in allPackages:
        if (package.deadline != "EOD") and package not in loadedPackages:
            if len(truck1.packages) < truck1.capacity:
                truck1.addPackage(package)
                loadedPackages.append(package)
            elif len(truck2.packages) < truck2.capacity:
                truck2.addPackage(package)
                loadedPackages.append(package)
    # Last, all remaining Packages are loaded into Trucks that are not at capacity
    for package in allPackages:
        if (package not in truck1.packages) and (package not in truck2.packages) and (package not in truck3.packages):
            if len(truck1.packages) < truck1.capacity:
                truck1.addPackage(package)
                loadedPackages.append(package)
            elif len(truck3.packages) < truck3.capacity:
                truck3.addPackage(package)
                loadedPackages.append(package)
            elif len(truck2.packages) < truck2.capacity:
                truck2.addPackage(package)
                loadedPackages.append(package)
    return [truck1, truck2, truck3]


# Finds the next closest Package to deliver until none remain
# Runs in O(N^2)
def findRoute(truck, packageList):
    while len(packageList) != 0:
        global totalMilesTraveled
        minDistance = 100.0
        nextPackage = None
        nextLocation = None
        for package in packageList:
            distance = float(package.location.getDistance(truck.location))
            if distance < minDistance:
                minDistance = distance
                nextPackage = package
                nextLocation = package.location
        truck.dropoffPackage(nextPackage, minDistance, nextLocation)
        totalMilesTraveled += minDistance
    return True


# Finds a route for and Delivers all Packages for a given Truck
# Runs in O(N^2)
def deliverPackages(truck):
    for package in truck.packages:
        package.status = "ON_ROUTE"
        package.updateStartTime(truck.currentTime)
    # Packages with a Deadline are always Delivered First
    findRoute(truck, truck.priorityPackages)
    if len(truck.priorityPackages) == 0:
        findRoute(truck, truck.packages)
    if len(truck.packages) == 0:
        distanceToHub = float(truck.location.getDistance(allLocations[0]))
        completionTime = truck.returnHome(distanceToHub)
        return completionTime, truck.milesTraveled
