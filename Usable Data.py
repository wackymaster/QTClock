##Plotting with Turtle##
from math import pi
import numpy as np
import csv
import matplotlib.pyplot as plt
import datetime
import time
from tkFileDialog import askopenfilename
import os
import Tkinter
from Tkinter import *
from Tkinter import Tk
time_format = '%Y-%m-%dT%H:%M:%S.%f'
file_location = ''
def plotCSV():
# Open CSV
    x = []
    y = []
    with open(file_location,'r') as csvfile:
        print('Recieving Data from CSV...')
        reader = csv.reader(csvfile,delimiter = ',')
        for row in reader:
            x.append(row[0])
            y.append(row[1])
    # Remove Header        
    x = x[1:]
    y = y[1:]

    # Filter Data
    counter1 = 0
    while(counter1 < len(x)):
        x[counter1] = time.strptime(x[counter1],time_format)# Convert Given Time to DateTime Format
        x[counter1] = datetime.timedelta(days=x[counter1].tm_mday,hours=x[counter1].tm_hour,minutes=x[counter1].tm_min,seconds=x[counter1].tm_sec).total_seconds()
        counter1 +=1
        
    first_time = x[1]
    last_time = x[-1]

    #x[:] = [float(a - first_time) for a in x]
    x[:] = [float(a/3600) for a in x]

    first_time = x[1]
    last_time = x[-1]
    degrees_total = (last_time/24)*360
    degrees = degrees_total/last_time
    time_difference = [float((a/last_time)*degrees_total) for a in x]
    counter2 = 0
    new_x = [float(a*degrees) for a in x]
    ax = plt.subplot(111, projection='polar')
    ax.set_theta_direction(-1)
    ax.set_theta_offset(pi/2.0)
    ax.set_xticks(np.linspace(0, 2*pi, 24, endpoint=False))
    ax.set_xticklabels(range(int(last_time+1)))
    ax.set_yticks((0.300,0.350,0.400,0.450,0.500,0.550,0.600))
    ax.set_ylim([0.3,0.6])
    ax.set_yticklabels(('300','350','400','450','500','550','600'))
    #ax.plot(np.deg2rad(new_x),y)
    ax.plot(np.deg2rad(time_difference),y)
    plt.show()

def findCSV():
    global file_location
    filename = askopenfilename()
    if(filename ==''):
        tkMessageBox.showinfo("Error", "Please Specify File")
    file_location = str(filename)
    found = True

    
def finished():
    global time_format
    time_format = E1.get()
    plotCSV()

# Gui- Don't even bother...    
top = Tkinter.Tk()
top.resizable(width=False, height=False)
top.geometry('{}x{}'.format(500, 500))
L1 = Label(top, text="Date Format")
E1 = Entry(top, bd =5)
E1.insert(0, '%Y-%m-%dT%H:%M:%S.%f')
Find = Tkinter.Button(top, text ="Find CSV", command = findCSV)
Done = Tkinter.Button(top, text ="Done", command = finished)
w = Tkinter.Label(top, text="QTClock",font=("Helvetica", 30))
w2 = Tkinter.Label(top, text="By Will Wang", font=("Helvetica", 8))
# Place Everything on Canvas Window
L1.place(relx=0.3625,rely=0.45)
E1.place(relx=0.3625,rely=0.4)
Find.place(relx=0.25,rely=0.4)
Done.place(relx=0.625,rely=0.4)
w.place(relx=0.35,rely=0.1)
w2.place(relx=0.35,rely=0.2)
top.mainloop()
