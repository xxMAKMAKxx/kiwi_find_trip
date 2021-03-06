#!/bin/python
# Created by Martin Kacmarcik
# for Kiwi.com Python weekend challenge
# tested on Python 2.7

import re
import sys

# define global variables
firstTime = False


def findCountryCodeByCountry(countryCode):
    f = open('data/country.dat', 'r')
    for line in f.readlines():
        if(re.search(countryCode, line)):
            line = re.sub("\".*\"(.*)", "\"\""+r'\1', line)
            splitLine = line.split(', ')
            splitLine[1] = re.sub('[!\n]', '', splitLine[1])
            return splitLine[1]


def findCountryByAirport(airportCode):
    f = open('data/airports.dat', 'r')
    for line in f.readlines():
        if(re.search(airportCode, line)):
            splitLine = line.split(', ')
            if(re.sub('[!\"]', '', splitLine[4]) == airportCode):
                return findCountryCodeByCountry(re.sub('[!\"]', '', splitLine[3]))


def findFirstTrip(sourceCity):
    input_file = open('data/input_data_nicer.csv', 'r')
    for line in input_file.readlines():
        line = re.sub('[!\n]', '', line)
        line = line.split(';')
        if(line[0] == sourceCity):
            return line


def DepthLimitedSearch(node, depth, firstFlight, i, arrayOfResults):
    input_file = open('data/input_data_nicer.csv', 'r')
    if(depth >= 0):
        for child in input_file.readlines():
            child = re.sub('[!\n]', '', child)
            child = child.split(';')
            if(not node):
                exit(2)
            if(node[1] == child[0] and node[3] < child[2]):
                if(depth == 0 and node[1] == firstFlight[0] and int(node[3]) < (int(firstFlight[2])+10000000000)):
                    return node
                else:
                    found = DepthLimitedSearch(child, depth-1, firstFlight, i, arrayOfResults)
                if(found is not None):
                    global firstTime
                    if(not firstTime):
                        firstTime = True
                        return child
                    arrayOfResults.append(str(str(i)+";"+findCountryByAirport(found[0])+";"+found[0]+";"+found[1]+";"+found[2]+";"+found[3]))
                    return child
    return None


def makeOutputHowItKiwiWants(item):
    item = re.sub("(.*;.*;.*;.*;)([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})[0-9]{2};([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})[0-9]{2}", r'\1'+r'\2'+"-"+r'\3'+"-"+r'\4'+"T"+r'\5'+":"+r'\6'+";"+r'\7'+"-"+r'\8'+"-"+r'\9'+"T"+r'\10'+":"+r'\11', item)
    return item


# Simple checks of args
if(len(sys.argv) != 3):
    print("I think we have a problem here... I need one parameter which is IATA code of an airport and one number which is index of the search")
    exit(0)
elif(len(sys.argv[1]) != 3):
    print("Need IATA code of an airport, check https://en.wikipedia.org/wiki/International_Air_Transport_Association_airport_code")


arrayOfResults = []
firstFlight = findFirstTrip(sys.argv[1])
returnedNode = DepthLimitedSearch(firstFlight, 9, firstFlight, sys.argv[2], arrayOfResults)
if(not returnedNode):
    exit(3)
arrayOfResults.append(str(sys.argv[2]+";"+findCountryByAirport(returnedNode[0])+";"+returnedNode[0]+";"+returnedNode[1]+";"+returnedNode[2]+";"+returnedNode[3]))
arrayOfResults.append(str(sys.argv[2]+";"+findCountryByAirport(firstFlight[0])+";"+firstFlight[0]+";"+firstFlight[1]+";"+firstFlight[2]+";"+firstFlight[3]))
for item in reversed(arrayOfResults):
    print makeOutputHowItKiwiWants(item)
