#!/usr/bin/python2.7
#


from pymongo import MongoClient
import os
import sys
import json

from math import cos, sin, sqrt, atan2, radians


def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):
    # Read the input in the cursor
    cursor = collection.find()
    # check for rows with city name as cityToSearch in the cursor and write the attributes name,
    # full address and state to output

    with open(saveLocation1, 'w') as output:
        for rows in cursor:
            if cityToSearch.lower() == rows['city'].lower():
                output.write(((rows['name'] + str('$') + rows['full_address'].replace("\n", ", ") + str('$') + rows['city'] + str('$') + rows['state'] + str('.\n')).upper()).encode("utf:8"))



def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):

    cursor = collection.find()

    with open(saveLocation2, 'w') as output:
        for rows in cursor:
            # pass latitude, longitude, business latitude and business latitude to distance and check if it is less than maxDistance
            if distance(rows['latitude'], rows['longitude'], float(myLocation[0]), float(myLocation[1])) < maxDistance:
                category_row = rows['categories']
                # for all categories in categoryToSearch write category name to output
                for category in categoriesToSearch:
                    if category in category_row:
                        output.write(((rows['name'] + str('\n')).upper()).encode("utf-8"))
                        break



def distance(lat2, lon2, lat1, lon1):
    r = 3959
    theta_1 = radians(lat1)
    theta_2 = radians(lat2)
    theta = radians(lat2 - lat1)
    lamda = radians(lon2 - lon1)
    a = sin(theta / 2) * sin(theta / 2) + cos(theta_1) * cos(theta_2) * sin(lamda / 2) * sin(lamda / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = r * c
    return d

