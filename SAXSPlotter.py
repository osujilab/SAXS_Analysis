# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:44:25 2023
SAXS Plotting Template
@author: Chris
The purpose of this code is to have a general-purpose
SAXS plotter that can interactively identify the peaks 
with minimal effort.
"""
#Formatting master sheet
#Import needed parameters
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd

#from matplotlib import ticker
from matplotlib.backend_bases import MouseButton





#print(mpl.font_manager.get_font_names())
mpl.rcParams['lines.linewidth'] = 2 #Visually change the width of lines
mpl.rcParams['lines.linestyle'] = '--'
mpl.rcParams['font.family'] = ['Liberation Sans', 'sans-serif']
mpl.rcParams['font.size'] = 8
mpl.rcParams['figure.figsize'] = [3, 3]
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams['font.sans-serif'] = 'Liberation Sans'
colors = ['b','g','r','c','m','y'] #Random list of colors, used for plotting

filename = "03062024_CJ_KC_1815.xlsx" #.xlsx
useful_range = [0.10, 0.3] #Input array of two floats with the range you want
scale = 50 #Input the scaling to see how it looks #Float
lblsz=8 #xtick label size
###
#Ideally, put all of the interpreted SAXS into a single file. Will add compatibility for multiple  files later
###
#Plotting parameters to follow





#Load saxs excel sheet
SAXS_FILE = pd.read_excel(filename, header=2) #index_col=0)

SAXS_FILE.fillna(0, inplace=True)
SAXS_FILE=SAXS_FILE.replace('--', 0)
traces = SAXS_FILE.shape[1]-1
print(SAXS_FILE)
#print(SAXS_FILE[1])
columns = list(SAXS_FILE)



#Plot excel sheet
fig, ax = plt.subplots(1,1)
topval = 0 #Need to get top ylim
for i in range(1,traces+1):
    x = SAXS_FILE[columns[0]].to_list()
    #print(x) Print to test the data put in if the graph doesn't work
    int_list = np.array(SAXS_FILE[columns[i]].to_list())
    y = int_list*(scale**(i))
    #print(y) Print to test the data put in if the graph doesn't work
    ax.plot(x,y, '-',lw=1.5,color=colors[i-1])
    if max(y) > topval:
        topval = max(y)

ax.set_yscale("log")
ax.set_xlim(useful_range)
ax.set_ylim(top=topval*3) #Note that this will only return the last list. Make sure that the 
#intensities aren't too different... otherwise this will get messy!
ax.tick_params(axis="y",direction="in", labelsize=lblsz)
ax.tick_params(axis="x",direction="in", labelsize=lblsz)
ax.minorticks_off()
ax.set_xlabel(r"q $(A^{-1})$",fontsize=lblsz*1.5)
ax.set_ylabel("I(q) (arb. units)")
ax.set_box_aspect(1)


plt.tight_layout()
fig.show()


#Define printed clicks


editing = True #Need to set edit state so while loop can functioln
def on_move(event):
    if event.inaxes:
        pass
        #print(f'data coords {event.xdata} {event.ydata}', f'pixel coords {event.x} {event.y}')
        
# def on_press(event):
#     #We want to determine the color of the text that we are pressing. 
#     #Enumerate the number of colors
#     print('pressed', event.key)
#     text_color = colors[int(event.key)] #Will only be able to access integers and 0-9. What about more colors? Consider this edge case 10 colors is a lot
#     if event.key=='x':
#         editing = False
    
text_color = 0 #Starting text color

def on_click(event):
    global text_color
    global a
    if event.button is MouseButton.LEFT:
        print('click registered')
        #Input x-coord on click
        a = plt.text(event.xdata+useful_range[0]*0.05, event.ydata*1.05, f'{(round(event.xdata, 3))} '+r'$A^{-1}$',fontsize=8,c=colors[text_color],ha='center')
        plt.draw()
    elif event.button is MouseButton.RIGHT:
        print('color changed')
         #Calling text_color
        text_color += 1
        print(text_color)
        if text_color > traces-1:
            text_color = 0 #Reset the color back to the start if we have less than 10 traces
            print('reset_color')
    elif event.button is MouseButton.MIDDLE:
        a.remove()
        plt.draw()
        
#def change_color(event)


binding_id = plt.connect('motion_notify_event',on_move)
#plt.connect('key_press_event', on_press)
plt.connect('button_press_event',on_click)
        

