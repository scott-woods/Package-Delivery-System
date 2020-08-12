# Name: Scott Woods
# Student ID: 001210376

import datetime
import sys
import ReadFiles
import Delivery


class Main:
    # Creates a Table of Packages using the PackageHashTable Class
    packageTable = ReadFiles.packageTable
    # Stores the time at which each Truck returns to the Hub
    completionTimes = []
    # Create and load a set of Trucks, and then have them Deliver all of their Packages
    trucks = ReadFiles.loadTrucks()
    truck1_completion = ReadFiles.deliverPackages(trucks[0])[0]
    truck2_completion = ReadFiles.deliverPackages(trucks[1])[0]
    completionTimes.append(truck1_completion)
    completionTimes.append(truck2_completion)
    # Updates the third Truck's start time to be the earliest time at which the first two trucks returns
    truck3_minStart = datetime.datetime(2020, 8, 1, 9, 5, 0)
    truck3_start = datetime.datetime.max
    # Runs in O(N)
    for time in completionTimes:
        if (time < truck3_start) and (time >= truck3_minStart):
            truck3_start = time
    trucks[2].updateTime(truck3_start)
    truck3_completion = ReadFiles.deliverPackages(trucks[2])[0]
    completionTimes.append(truck3_completion)

    print("Total Miles Traveled: {}".format(ReadFiles.totalMilesTraveled))
    print("All Packages Delivered by: {}".format(max(completionTimes)))
    print("Total Packages Delivered: {}".format(len(Delivery.deliveredPackages)))

    print("\nWelcome to the WGUPS Package Delivery System!")

    active = True
    while active:
        print("Please select from one of the following options: ")
        print("1. Package Info")
        print("2. Lookup Package Status by Time")
        print("3. Show All Package Info")
        print("4. Show All Package Info by Time")
        print("5. Exit Program")
        startSelection = input("\nEnter the number of your selection here: ")
        # Lookup the Info for one Package by its ID
        if startSelection == '1':
            lookupKey = input("\nPlease enter the Package ID of the Package you are looking for: ")
            packageInfo = packageTable.search(lookupKey)
            # Print info formatted for better readability in Command Line
            print("\nHere are the details for that Package: \n\nPackage ID: {} \nAddress: {} \nCity: {} "
                  "\nState: {} \nZIP: {} \nDeadline: {} "
                  "\nWeight: {} \nNotes: {} \nStatus: {} \nDelivery Time: {}".format(packageInfo.packageID,
                                                                                     packageInfo.address,
                                                                                     packageInfo.city,
                                                                                     packageInfo.state,
                                                                                     packageInfo.postalCode,
                                                                                     packageInfo.deadline,
                                                                                     packageInfo.weight,
                                                                                     packageInfo.notes,
                                                                                     packageInfo.status,
                                                                                     packageInfo.deliveryTime))
            restartPrompt = input("\nReturn to Menu? (Y/N): ")
            if restartPrompt == 'Y':
                active = True
            elif restartPrompt == 'N':
                print("Have a Great Day!")
                active = False
                sys.exit()
        # Look up the Info for one Package at a specific time by its ID
        if startSelection == '2':
            lookupKey = input("\nPlease enter a Package ID: ")
            packageInfo = packageTable.search(lookupKey)
            print("Please enter a time on the 24-Hour clock in the following format: HH:MM:SS")
            inputTime = input("Enter Here: ")
            (h, m, s) = inputTime.split(":")
            inputDatetime = datetime.datetime.today().replace(hour=int(h), minute=int(m), second=int(s), microsecond=0)
            infoAtTime = packageInfo.getAllInfo(inputDatetime)
            print(infoAtTime)
            if packageInfo.deliveryTime > inputDatetime > packageInfo.startTime:
                print("The Status of Package {} at {} is ON_ROUTE".format(packageInfo.packageID, inputDatetime))
            elif packageInfo.deliveryTime < inputDatetime:
                print("The Status of Package {} at {} is DELIVERED".format(packageInfo.packageID, inputDatetime))
            elif inputDatetime < packageInfo.startTime:
                print("The Status of Package {} at {} is AT_HUB".format(packageInfo.packageID, inputDatetime))
            restartPrompt = input("\nReturn to Menu? (Y/N): ")
            if restartPrompt == 'Y':
                active = True
            elif restartPrompt == 'N':
                print("Have a Great Day!")
                active = False
                sys.exit()
        # Show the Info for every Package
        if startSelection == '3':
            for package in Delivery.allPackages:
                info = package.getAllInfo(package.deliveryTime)
                print(info)
            restartPrompt = input("\nReturn to Menu? (Y/N): ")
            if restartPrompt == 'Y':
                active = True
            elif restartPrompt == 'N':
                print("Have a Great Day!")
                active = False
                sys.exit()
        # Show the Info for every Package at a specific time
        if startSelection == '4':
            print("\nPlease enter a time on the 24-Hour clock in the following format: HH:MM:SS")
            inputTime = input("Enter Here: ")
            (h, m, s) = inputTime.split(":")
            inputDatetime = datetime.datetime.today().replace(hour=int(h), minute=int(m), second=int(s), microsecond=0)
            print("Here is the Info for all Packages at {}".format(inputDatetime))
            for package in Delivery.allPackages:
                infoAtTime = package.getAllInfo(inputDatetime)
                print(infoAtTime)
            restartPrompt = input("\nReturn to Menu? (Y/N): ")
            if restartPrompt == 'Y':
                active = True
            elif restartPrompt == 'N':
                print("Have a Great Day!")
                active = False
                sys.exit()
        # Exit the Program
        if startSelection == '5':
            print("Thank you for using the WGUPS Package Delivery System!")
            active = False
            sys.exit()
