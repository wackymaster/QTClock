##Plotting with Turtle##
from turtle import *
import turtle
import random
import numpy
import math
from math import pi
import numpy as np
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os
import Tkinter
from Tkinter import *
from Tkinter import Tk
from tkFileDialog import askopenfilename
import tkMessageBox
import subprocess

#Turtle Prog
Lines = []
Connections = []
lineColors = []
lineNames = []
startingTimes = []
found = False
csv_location = ""
filename = ""
date_format = ""
def parseConcentrations(data, tformat):
    conX = data[0]
    conY = data[1]
    timePlacements = []
    cons = []
    #Split into X and Y/
    conC = 0
    while(conC < len(conX)):
        currentTime = conX[conC]
        currentTime = currentTime.translate(None,':')
        currentTime = datetime.strptime(currentTime,tformat)
        timePlacements.append(360 * (float(currentTime.hour) / 24.0))
        #print(timePlacements[conC])
        conC += 1
    cscounter, setCounter, thisCon, previousInterpolate, cic = 0, 0, 0, 0 ,0
    nextCon, previousCon = conY[0], conY[0]
    while(cscounter < 360):
        if(cscounter == timePlacements[setCounter]) & (setCounter < len(timePlacements)):
            cons.append(conY[setCounter])
            thisCon = conY[setCounter]
            previousInterpolate = thisCon
            previousCon = conY[setCounter]
            if(setCounter < len(timePlacements) - 1):
                setCounter += 1
                cic = timePlacements[setCounter] - timePlacements[setCounter - 1]
                nextCon = conY[setCounter]
        else:
            thisCon = float(previousInterpolate) - ((float(previousCon) - float(nextCon)) / float(cic))
            previousInterpolate = thisCon
            cons.append(thisCon)
        cscounter += 1
    print(cons)
    print(len(cons))
    return(cons)
    #RETURN A 360 length array of concentrations smoothed
    
def readData(fileName, header = True):
    x = []
    y = []
    with open(fileName,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter = ',')
        for row in reader:
            x.append(row[0])
            y.append(row[1])
    if(header == True):
        x = x[1:]
        y = y[1:]
    rData = [x,y]
    return(rData)
def parseData(data,dateFormat,length,smoothing = 1, yScale = 1000):
    dataX = data[0] 
    dataY = data[1]
    #Get the first day
    startingTimes.append(dataX[0])
    firstTime = 0
    firstDay = 0
    percentage = 0
    #================#
    firstSample = dataX[0]
    firstSample = firstSample.translate(None,':')
    firstSample = firstSample[:length]
    firstSample = datetime.strptime(firstSample, dateFormat)
    firstTime = firstSample.time()
    firstDay = firstSample.day
    #================#
    ##Making new data set
    newX = []
    newY = []
    dataCounter = 0
    while(dataCounter < len(dataX)):
        percentage = float(dataCounter) / float(len(dataX))
        percentage = percentage * 100
       # print("%%%1.2f parsing.. "%percentage)
        #convert the x
        currentX = dataX[dataCounter]
        currentY = dataY[dataCounter]
        #Filter the current x to a datetime
        currentX = currentX.translate(None,':')
        currentX = currentX[:length]
        currentX = datetime.strptime(currentX, dateFormat)
        if(currentX.day == firstDay) | (firstTime < currentX.time()): 
            #Convert to 'weird' time
            currentX = str(currentX.time())
            currentX = currentX.translate(None,':')
            currentX = float(currentX)
            currentY = int(1000 * float(currentY))
            newX.append(currentX)
            newY.append(currentY)
        dataCounter += 1
    newData = [newX,newY]
    if(smoothing > 1):
        print("Smoothing data.. ")
        smoothCounter = 0
        smoothX = []
        smoothY = []
        while(smoothCounter < (len(newX) / smoothing)):
            indexT = 0
            indexF = smoothCounter * smoothing
            indexT = indexF + smoothing
            smoothedX = numpy.mean(newX[indexF:indexT])
            smoothedY = numpy.mean(newY[indexF:indexT])
            smoothX.append(smoothedX)
            smoothY.append(smoothedY)
            smoothCounter += 1
        smoothedData = [smoothX,smoothY]
        return(smoothedData)
    else:
        return(newData)
    #return(newData)
    #Parse x , y data (qtcb, etc..) into readable time and qtcb
def everything():
    xcounter1 = 0
    xcounter2 = 0
    xLength1 = random.randint(2,1000)
    xLength2 = random.randint(2,1000)
    xList = []
    xList2 = []
    yList = []
    yList2 = []
    while(xcounter1 < xLength1):
        xVal = xcounter1
        yVal = random.randint(0,100)
        xList.append(xVal)
        yList.append(yVal)
        xcounter1 += 1
    while(xcounter2 < xLength2):
        xVal = xcounter1
        yVal = random.randint(0,100)
        xList2.append(xVal)
        yList2.append(yVal)
        xcounter2 += 1

    print("Retrieving Data...")
    theDat = readData(csv_location)
    print("Data Received")
    print("Parsing Data...")
    theDatx = theDat[0]
    theDaty = theDat[1]
    newDAT = [theDatx[0:1000],theDaty[0:1000]]
    someDat = parseData(theDat,date_format,17,smoothing = 1000,yScale = 1000)
    first_x = theDatx[1]
    blaa = len(theDatx)
    ax = plt.subplot(111, polar=True)
    first_x = first_x[11:16]
    hours_x = float(first_x[:2])
    minutes_x = first_x[-2:]
    minutes_x = (float(minutes_x))/60
    final_x = hours_x + minutes_x
    equals = np.linspace(0, 360, blaa, endpoint=False) #np.arange(24)
    ones = np.ones(blaa)


    plt.plot(np.deg2rad(equals), theDaty)       

        # Set the circumference labels
    ax.set_xticks(np.linspace(0, 2*np.pi, 24, endpoint=False))
    ax.set_xticklabels(range(24))
    ax.set_yticks((0.300,0.350,0.400,0.450,0.500,0.550,0.600))
    ax.set_ylim([0.3,0.6])
    ax.set_yticklabels(('300','350','400','450','500','550','600'))
        # Make the labels go clockwise
    ax.set_theta_direction(-1)       

        # Place 0 at the top
    ax.set_theta_offset(np.pi/2.0)

    
    plt.show()

top = Tkinter.Tk()
top.resizable(width=False, height=False)
top.geometry('{}x{}'.format(500, 500))
def findCSV():
   #subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')
   global filename
   global found
   global csv_location
   
   filename = askopenfilename()
   if(filename ==''):
       tkMessageBox.showinfo("Error", "Please Specify File")
   csv_location = str(filename)
   found = True
   print(csv_location)
def finished():
    global date_format
    date_format = E1.get()
    if(date_format == ''):
        date_format = '%Y-%m-%dT%H%M%S'
    if(date_format == 'Date Format'):
        date_format = '%Y-%m-%dT%H%M%S'
    if(found == True):
        everything()
    else:
        tkMessageBox.showinfo("Error", "Please Specify File")
L1 = Label(top, text="(Leave Blank for Default)")
E1 = Entry(top, bd =5)
E1.insert(0, 'Date Format')
Find = Tkinter.Button(top, text ="Find CSV", command = findCSV)
Done = Tkinter.Button(top, text ="Done", command = finished)
w = Tkinter.Label(top, text="QTClock",font=("Helvetica", 30))
w2 = Tkinter.Label(top, text="By Will Wang and Rowan McNitt", font=("Helvetica", 8))
# Place Everything on Canvas Window
L1.place(relx=0.3625,rely=0.45)
E1.place(relx=0.3625,rely=0.4)
Find.place(relx=0.25,rely=0.4)
Done.place(relx=0.625,rely=0.4)
w.place(relx=0.35,rely=0.1)
w2.place(relx=0.35,rely=0.2)
top.mainloop()
