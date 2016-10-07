##Plotting with Turtle##
from math import pi
import numpy as np
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
import time
from tkFileDialog import askopenfilename
import os
import Tkinter
from Tkinter import *
from Tkinter import Tk
import tkMessageBox
import multiprocessing as mp
time_format = '%Y-%m-%dT%H:%M:%S.%f'
file_location = ''
time_array = ''
qt_array = ''

  
def plotCSV():
# Open CSV
    try:
        x = []
        y = []
        z = []
        start_time = time.time()
        with open(file_location,'r') as csvfile:
            print('Recieving Data from CSV...')
            reader = csv.reader(csvfile,delimiter = ',')
            for row in reader:
                global time_array
                global qt_array
                x.append(row[time_array])
                y.append(row[qt_array])

        # Remove Header        
        x = x[1:]
        y = y[1:]

        # Filter Data
        counter1 = 0
        print('Converting To Date...')
        while(counter1 < len(x)):
            x[counter1] = time.strptime(x[counter1],time_format)# Convert Given Time to DateTime Format
            x[counter1] = datetime.timedelta(days=x[counter1].tm_mday,hours=x[counter1].tm_hour,minutes=x[counter1].tm_min,seconds=x[counter1].tm_sec).total_seconds()
            counter1 +=1
            
        first_time = x[1]
        last_time = x[-1]
        print('Converting to Hours...')
        #x[:] = [float(a - first_time) for a in x]
        x[:] = [float(a/3600) for a in x]
        print('Generating Plot...')
        first_time = x[1]
        last_time = x[-1]
        print('Calculating Degrees...')
        degrees_total = (last_time/24)*360
        degrees = degrees_total/last_time
        print('Plotting...')
        x = [float((a/last_time)*degrees_total) for a in x]
        ax = plt.subplot(111, projection='polar')
        ax.set_theta_direction(-1)
        ax.set_theta_offset(pi/2.0)
        #ax.set_xticks(np.linspace(0, 2*pi, 24, endpoint=False))
        #ax.set_xticklabels(range(int(last_time+1)))
        ax.set_xticklabels(['00:00', '03:00', '06:00', '09:00',
                                 '12:00', '15:00', '18:00', '21:00'])
        ax.set_yticks((0.300,0.350,0.400,0.450,0.500,0.550,0.600))
        ax.set_ylim([0.3,0.6])
        ax.set_yticklabels(('300','350','400','450','500','550','600'))
        file_name = os.path.basename(file_location)
        ax.plot(np.deg2rad(x),y, label = file_name)
        ax.legend(loc="upper left", bbox_to_anchor=(1,1.1))
        elapsed_time = time.time() - start_time
        print('Done in:', elapsed_time, 'seconds')
        plt.show()
    except Exception, e:
        error_message = 'Error'
        tkMessageBox.showinfo('Error',  str(e))
def findCSV():
    global file_location
    filename = askopenfilename()
    if(filename ==''):
        tkMessageBox.showinfo("Error", "Please Specify File")
    file_location = str(filename)
    found = True


def finished():
    global time_format
    global time_array
    global qt_array
    time_format = E1.get()
    time_array = int(E2.get())
    qt_array = int(E3.get())
    plotCSV()

if __name__=='__main__':
    mp.freeze_support()  # only needed in Windows
    #GUI
    top = Tkinter.Tk()
    top.resizable(width=False, height=False)
    top.geometry('{}x{}'.format(500, 500))
    L1 = Label(top, text="Date Format")
    L2 = Label(top, text="Time Row")
    L3 = Label(top, text="QT Row")
    E1 = Entry(top, bd =5)
    E1.insert(0, '%Y-%m-%dT%H:%M:%S.%f')
    E2 = Entry(top, bd =2)
    E2.insert(0, '0')
    E3 = Entry(top, bd =2)
    E3.insert(0, '1')
    Find = Tkinter.Button(top, text ="Find CSV", command = findCSV)
    Done = Tkinter.Button(top, text ="Done", command = finished)
    w = Tkinter.Label(top, text="QTClock",font=("Helvetica", 30))
    w2 = Tkinter.Label(top, text="By Will Wang", font=("Helvetica", 8))
    # Place Everything on Canvas Window
    L1.place(relx=0.3625,rely=0.45)
    L2.place(relx=0.225,rely=0.55)
    L3.place(relx=0.35,rely=0.55)
    E1.place(relx=0.3625,rely=0.4)
    E2.place(relx=0.25,rely=0.5, width = 40)
    E3.place(relx=0.35,rely=0.5, width = 40)
    Find.place(relx=0.25,rely=0.4)
    Done.place(relx=0.625,rely=0.4)
    w.place(relx=0.35,rely=0.1)
    w2.place(relx=0.35,rely=0.2)
    top.mainloop()
