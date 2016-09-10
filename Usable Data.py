##Plotting with Turtle##
from math import pi
import numpy as np
import csv
import matplotlib.pyplot as plt
import datetime
import time
x = []
y = []
# Open CSV
with open('baseline_eg.csv','r') as csvfile:
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
    x[counter1] = time.strptime(x[counter1],'%Y-%m-%dT%H:%M:%S.%f')# Convert Given Time to DateTime Format
    x[counter1] = datetime.timedelta(days=x[counter1].tm_mday,hours=x[counter1].tm_hour,minutes=x[counter1].tm_min,seconds=x[counter1].tm_sec).total_seconds()
    counter1 +=1
    
first_time = x[1]
last_time = x[-1]
x[:] = [float(a - first_time) for a in x]
x[:] = [float(a/3600) for a in x]
first_time = x[1]
last_time = x[-1]
print(first_time, last_time)

# Plot
ax = plt.subplot(111, projection='polar')
ax.set_theta_direction(-1)
ax.set_theta_offset(pi/2.0)
ax.set_xticks(np.linspace(0, 2*pi, 24, endpoint=False))
ax.set_xticklabels(range(24))
ax.set_yticks((0.300,0.350,0.400,0.450,0.500,0.550,0.600))
ax.set_ylim([0.3,0.6])
ax.set_yticklabels(('300','350','400','450','500','550','600'))
ax.plot(x,y)
plt.show()
