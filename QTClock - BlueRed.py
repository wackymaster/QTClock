# User Variables
savepng = False # Change to True if you want Clock to be saved as PNG

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
time_array = ''
qt_array = ''
enableCon = ''
counter = 0

def getCSV(file_location, time_format, time_array, qt_array, enableCon):
    # Open CSV
    x, y, z = [], [], []
    with open(file_location,'r') as csvfile:
        print('Recieving Data from CSV...')
        reader = csv.reader(csvfile,delimiter = ',')
        for row in reader:
            x.append(row[time_array])
            y.append(row[qt_array])
            if (enableCon == 1):
                if row[2] in (None, ""):
                    z.append(-1)
                else:
                    z.append(row[2])
            if(enableCon == 0):
                z= [1,1,1]
        # Remove Header        
        x = x[1:]
        y = y[1:]
        z = z[1:]
        filterData(x,y, time_format,z, enableCon)

        
def filterData (x,y,time_format,z, enableCon):
        counter1, counterz = 0, 0
        # Convert To Python Date Format
        print('Converting To Date...')
        while(counter1 < len(x)):
            x[counter1] = time.strptime(x[counter1],time_format)# Convert Given Time to DateTime Format
            x[counter1] = datetime.timedelta(days=x[counter1].tm_mday,hours=x[counter1].tm_hour,minutes=x[counter1].tm_min,seconds=x[counter1].tm_sec).total_seconds()
            counter1 +=1
        counter = 0
        z_new = []
        z_new2 = []
        print(len(z)/3500)
        if enableCon == 1:
            while counter < len(z)/3500:
                z_chunk = z[int(counter*3500):int((counter+1))*3500]
                i = 1
                while i <len(z_chunk):
                    if z_chunk[i]==-1:
                        pass
                    if z_chunk[i]!=-1:
                        z_new.append(float(z_chunk[i]))
                    i += 1
                #print(z_new)
                
                z_new2.append((sum(z_new)/len(z_new)))
                del z_new[:]
                z_new.append(0)
                print(z_new2)
                counter += 1
            z=z_new2
        first_time = x[1]
        last_time = x[-1]
        print('Converting to Hours...')
        # Calculate degree value amount for each point
        x[:] = [float(a/3600) for a in x]
        print('Generating Plot...')
        first_time = x[1]
        last_time = x[-1]
        print('Calculating Degrees...')
        degrees_total = (last_time/24)*360
        degrees = degrees_total/last_time
        print('Plotting...')
        x = [float((a/last_time)*degrees_total) for a in x]
        plotCSV(x,y,z)

def plotCSV(x,y,z):
    global counter

    concentrations = z
    amounts = (len(x)+len(y))/2
    amount_per_hour = int(amounts/len(concentrations))
    print(amount_per_hour)
    # Create Polar Sublot
    ax = plt.subplot(111, projection='polar')
    ax.set_theta_direction(-1) # Make Plot Go in Right Direction
    ax.set_theta_offset(pi/2.0)# Put 0 on top
    ax.set_xticklabels(['00:00', '03:00', '06:00', '09:00',
                        '12:00', '15:00', '18:00', '21:00'])
    ax.set_yticks((0.300,0.350,0.400,0.450,0.500,0.550,0.600))
    ax.set_ylim([0.3,0.6])
    ax.set_yticklabels(('300','350','400','450','500','550','600'))
    file_name = os.path.basename(file_location)
    hour_counter = 0
    
    while hour_counter < len(concentrations):
        color_variant = concentrations[hour_counter]
        rgb_variant = float(color_variant)*255
        red_variance = float(color_variant)*255
        blue_variance = (1-(float(color_variant)))*255
        rgb_value = (red_variance,0,blue_variance)
        hex_value = '#%02x%02x%02x' % rgb_value
        reps = amount_per_hour * hour_counter
        x_chunk = x[int(reps):int(reps + amount_per_hour)]
        y_chunk = y[int(reps):int(reps + amount_per_hour)]
        color_graph = '0.75'
        ax.plot(np.deg2rad(x_chunk),y_chunk,color = hex_value)
        hour_counter +=1
    if counter == 0:
        theta = np.linspace(0, 2*np.pi, 100)
        ax.fill_between(theta, 0.5, ax.get_ylim()[1],
                        color='red', alpha=0.2, linewidth=0,
                        zorder=-1, label="danger")
        ax.fill_between(theta, 0.367, 0.435,
                        color='green', alpha=0.2, linewidth=0, zorder=-1,
                        label="healthy")
        counter +=1
    ax.legend(loc="upper left", bbox_to_anchor=(1,1.1))
    if savepng:
        plt.savefig(str(file_name + ".png"))
    plt.show()
    

      
    

        
def findCSV():
    global file_location
    filename = askopenfilename()
    if(filename ==''):
        tkMessageBox.showinfo("Error", "Please Specify File")
    file_location = str(filename)
    found = True


def finished():
    time_format = E1.get()
    time_array = int(E2.get())
    qt_array = int(E3.get())
    enableCon = int(conBool.get())
    print(enableCon)
    getCSV(file_location, time_format, time_array, qt_array, enableCon)

    
if __name__=='__main__':
    
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
    conBool = IntVar()
    conCheck = Tkinter.Checkbutton(top,text="Enable Concentrations", variable = conBool)
    conCheck.var = conBool
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
    conCheck.place(relx=0.45, rely=0.5)
    top.mainloop()
