# -- coding: utf-8 --
"""
Created on Sat Sep 17 15:39:09 2022

@author: ajusd
"""

from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import numpy as np

link1 = 25.2 #upper arm len
link2 = 9.4 #lower arm len
link3 = 17.6 #wrist len

#initial position
theta1 = float(np.deg2rad(90)) #shoulder-upper arm
theta2 = float(np.deg2rad(-130)) #upper-lower arm
theta3 = float(np.deg2rad(40)) #lower arm-wrist

z = link1*np.sin(theta1) + link2*np.sin(theta1 + theta2) + link3*np.sin(theta1 + theta2 + theta3)
x = link1*np.cos(theta1) + link2*np.cos(theta1 + theta2) + link3*np.cos(theta1 + theta2 + theta3)

print("x: ", x, "z: ", z)
def plot():
    global output, fig, theta3
    
    fig = Figure(figsize = (5, 5),
                    dpi = 100)
    
    plot1 = fig.add_subplot(111)
    
    # b = x - link3*np.cos(theta3)
    # c = np.sqrt(b*2 + z*2)
    # alpha1 = np.arctan(z/b)


    # alpha2 = (link1*2 + c - link2*2)/(2*link1*c)
    # if(alpha2 >= 0.54):
    #    alpha2 = np.arccos(np.minimum(1, alpha2))
    # else:
    #    alpha2 = np.arccos(np.maximum(-1, alpha2))

    # theta1 = alpha1 + alpha2 #degree 1

    # theta2 = (link1*2 + link2 - c*2)/(2*link1*link2) #degree 2
    # if(theta2 >= 0.54):
    #    theta2 = np.pi - np.arccos(np.minimum(1, theta2))
    # else:
    #    theta2 = np.pi - np.arccos(np.maximum(-1, theta2))

    # beta1 = (link2*2 + c - link1*2)/(2*link2*c)
    # if(beta1 >= 0.54):
    #    beta1 = np.arccos(np.minimum(1, beta1))
    # else:
    #    beta1 = np.arccos(np.maximum(-1, beta1))
    # beta2 = np.arctan(b/z)

    # theta3 = beta1 + beta2 + 1.5708 - np.pi

    servo1 = theta1
    servo2 = theta2
    servo3 = theta3

    print("Servo1\t: ",np.rad2deg(servo1))
    print("Servo2\t: ",np.rad2deg(servo2))
    print("Servo3\t: ",np.rad2deg(servo3))

    # plot1.figure(figsize=(6, 6))
    plot1.plot([0, link1*np.cos(servo1)], [0, link1*np.sin(servo1)], label='upper_arm', marker='.')

    plot1.plot( [link1*np.cos(servo1), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2)], 
            [link1*np.sin(servo1), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2)], 
            label='lower_arm', marker='.')
    plot1.plot([link1*np.cos(servo1) + link2*np.cos(servo1 + servo2), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2) + link3*np.cos(servo1+servo2+servo3)], 
            [link1*np.sin(servo1) + link2*np.sin(servo1 + servo2), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2) + link3*np.sin(servo1+servo2+servo3)], 
            label='wrist', marker='.')
    plot1.grid(True)
    plot1.legend()
    plot1.set_xlim(-50, 50)
    plot1.set_ylim(-50, 50) 

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    output = FigureCanvasTkAgg(fig, master = canvas)
    output.draw()

    # placing the canvas on the Tkinter window 
    output.get_tk_widget().pack()
    plot_button.destroy()
    up_button.pack()
    up_button.place(x=310, y=500)
    down_button.pack()
    down_button.place(x=310, y=600)
    left_button.pack()
    left_button.place(x=250, y=550)
    right_button.pack()
    right_button.place(x=370, y=550)

def up():
    global output, fig, z, theta3
    if output:
        for child in canvas.winfo_children():
            child.destroy()
        # or just use canvas.winfo_children()[0].destroy()  
  
    output = None
    z = z+1
    
    
    fig = Figure(figsize = (5, 5),
                    dpi = 100)
    
    plot1 = fig.add_subplot(111)
    
    b = x - link3*np.cos(theta3)
    c = np.sqrt(b**2 + z**2)
    alpha1 = np.arctan(z/b)


    alpha2 = (link1**2 + c**2 - link2**2)/(2*link1*c)
    if(alpha2 >= 0.54):
       alpha2 = np.arccos(np.minimum(1, alpha2))
    else:
       alpha2 = np.arccos(np.maximum(-1, alpha2))

    theta1 = alpha1 + alpha2 #degree 1

    theta2 = (link1**2 + link2**2 - c**2)/(2*link1*link2) #degree 2
    if(theta2 >= 0.54):
       theta2 = np.pi - np.arccos(np.minimum(1, theta2))
    else:
       theta2 = np.pi - np.arccos(np.maximum(-1, theta2))

    beta1 = (link2**2 + c**2 - link1**2)/(2*link2*c)
    if(beta1 >= 0.54):
       beta1 = np.arccos(np.minimum(1, beta1))
    else:
       beta1 = np.arccos(np.maximum(-1, beta1))
    beta2 = np.arctan(b/z)

    theta3 = beta1 + beta2 + 1.5708 - np.pi

    servo1 = theta1
    servo2 = -theta2
    servo3 = theta3

    print("Servo1\t: ",np.rad2deg(servo1))
    print("Servo2\t: ",np.rad2deg(servo2))
    print("Servo3\t: ",np.rad2deg(servo3))

    # plot1.figure(figsize=(6, 6))
    plot1.plot([0, link1*np.cos(servo1)], [0, link1*np.sin(servo1)], label='upper_arm', marker='.')

    plot1.plot( [link1*np.cos(servo1), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2)], 
            [link1*np.sin(servo1), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2)], 
            label='lower_arm', marker='.')
    plot1.plot([link1*np.cos(servo1) + link2*np.cos(servo1 + servo2), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2) + link3*np.cos(servo1+servo2+servo3)], 
            [link1*np.sin(servo1) + link2*np.sin(servo1 + servo2), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2) + link3*np.sin(servo1+servo2+servo3)], 
            label='wrist', marker='.')
    plot1.grid(True)
    plot1.legend()
    plot1.set_xlim(-50, 50)
    plot1.set_ylim(-50, 50) 

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    output = FigureCanvasTkAgg(fig, master = canvas)
    output.draw()

    # placing the canvas on the Tkinter window 
    output.get_tk_widget().pack()
    
def down():
    global output, fig, z, theta3
    if output:
        for child in canvas.winfo_children():
            child.destroy()
        # or just use canvas.winfo_children()[0].destroy()  
  
    output = None
    z = z-1
    
    
    fig = Figure(figsize = (5, 5),
                    dpi = 100)
    
    plot1 = fig.add_subplot(111)
    
    b = x - link3*np.cos(theta3)
    c = np.sqrt(b**2 + z**2)
    alpha1 = np.arctan(z/b)


    alpha2 = (link1**2 + c**2 - link2**2)/(2*link1*c)
    if(alpha2 >= 0.54):
       alpha2 = np.arccos(np.minimum(1, alpha2))
    else:
       alpha2 = np.arccos(np.maximum(-1, alpha2))

    theta1 = alpha1 + alpha2 #degree 1

    theta2 = (link1**2 + link2**2 - c**2)/(2*link1*link2) #degree 2
    if(theta2 >= 0.54):
       theta2 = np.pi - np.arccos(np.minimum(1, theta2))
    else:
       theta2 = np.pi - np.arccos(np.maximum(-1, theta2))

    beta1 = (link2**2 + c**2 - link1**2)/(2*link2*c)
    if(beta1 >= 0.54):
       beta1 = np.arccos(np.minimum(1, beta1))
    else:
       beta1 = np.arccos(np.maximum(-1, beta1))
    beta2 = np.arctan(b/z)

    theta3 = beta1 + beta2 + 1.5708 - np.pi

    servo1 = theta1
    servo2 = -theta2
    servo3 = theta3

    print("Servo1\t: ",np.rad2deg(servo1))
    print("Servo2\t: ",np.rad2deg(servo2))
    print("Servo3\t: ",np.rad2deg(servo3))

    # plot1.figure(figsize=(6, 6))
    plot1.plot([0, link1*np.cos(servo1)], [0, link1*np.sin(servo1)], label='upper_arm', marker='.')

    plot1.plot( [link1*np.cos(servo1), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2)], 
            [link1*np.sin(servo1), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2)], 
            label='lower_arm', marker='.')
    plot1.plot([link1*np.cos(servo1) + link2*np.cos(servo1 + servo2), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2) + link3*np.cos(servo1+servo2+servo3)], 
            [link1*np.sin(servo1) + link2*np.sin(servo1 + servo2), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2) + link3*np.sin(servo1+servo2+servo3)], 
            label='wrist', marker='.')
    plot1.grid(True)
    plot1.legend()
    plot1.set_xlim(-50, 50)
    plot1.set_ylim(-50, 50) 

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    output = FigureCanvasTkAgg(fig, master = canvas)
    output.draw()

    # placing the canvas on the Tkinter window 
    output.get_tk_widget().pack()

def right():
    global output, fig, x, theta3
    if output:
        for child in canvas.winfo_children():
            child.destroy()
        # or just use canvas.winfo_children()[0].destroy()  
  
    output = None
    x = x+1
    
    
    fig = Figure(figsize = (5, 5),
                    dpi = 100)
    
    plot1 = fig.add_subplot(111)
    
    b = x - link3*np.cos(theta3)
    c = np.sqrt(b**2 + z**2)
    alpha1 = np.arctan(z/b)


    alpha2 = (link1**2 + c**2 - link2**2)/(2*link1*c)
    if(alpha2 >= 0.54):
       alpha2 = np.arccos(np.minimum(1, alpha2))
    else:
       alpha2 = np.arccos(np.maximum(-1, alpha2))

    theta1 = alpha1 + alpha2 #degree 1

    theta2 = (link1**2 + link2**2 - c**2)/(2*link1*link2) #degree 2
    if(theta2 >= 0.54):
       theta2 = np.pi - np.arccos(np.minimum(1, theta2))
    else:
       theta2 = np.pi - np.arccos(np.maximum(-1, theta2))

    beta1 = (link2**2 + c**2 - link1**2)/(2*link2*c)
    if(beta1 >= 0.54):
       beta1 = np.arccos(np.minimum(1, beta1))
    else:
       beta1 = np.arccos(np.maximum(-1, beta1))
    beta2 = np.arctan(b/z)

    theta3 = beta1 + beta2 + 1.5708 - np.pi

    servo1 = theta1
    servo2 = -theta2
    servo3 = theta3

    print("Servo1\t: ",np.rad2deg(servo1))
    print("Servo2\t: ",np.rad2deg(servo2))
    print("Servo3\t: ",np.rad2deg(servo3))

    # plot1.figure(figsize=(6, 6))
    plot1.plot([0, link1*np.cos(servo1)], [0, link1*np.sin(servo1)], label='upper_arm', marker='.')

    plot1.plot( [link1*np.cos(servo1), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2)], 
            [link1*np.sin(servo1), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2)], 
            label='lower_arm', marker='.')
    plot1.plot([link1*np.cos(servo1) + link2*np.cos(servo1 + servo2), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2) + link3*np.cos(servo1+servo2+servo3)], 
            [link1*np.sin(servo1) + link2*np.sin(servo1 + servo2), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2) + link3*np.sin(servo1+servo2+servo3)], 
            label='wrist', marker='.')
    plot1.grid(True)
    plot1.legend()
    plot1.set_xlim(-50, 50)
    plot1.set_ylim(-50, 50) 

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    output = FigureCanvasTkAgg(fig, master = canvas)
    output.draw()

    # placing the canvas on the Tkinter window 
    output.get_tk_widget().pack()

def left():
    global output, fig, x, theta3
    if output:
        for child in canvas.winfo_children():
            child.destroy()
        # or just use canvas.winfo_children()[0].destroy()  
  
    output = None
    x = x-1
    
    
    fig = Figure(figsize = (5, 5),
                    dpi = 100)
    
    plot1 = fig.add_subplot(111)
    
    b = x - link3*np.cos(theta3)
    c = np.sqrt(b**2 + z**2)
    alpha1 = np.arctan(z/b)


    alpha2 = (link1**2 + c**2 - link2**2)/(2*link1*c)
    if(alpha2 >= 0.54):
       alpha2 = np.arccos(np.minimum(1, alpha2))
    else:
       alpha2 = np.arccos(np.maximum(-1, alpha2))

    theta1 = alpha1 + alpha2 #degree 1

    theta2 = (link1**2 + link2**2 - c**2)/(2*link1*link2) #degree 2
    if(theta2 >= 0.54):
       theta2 = np.pi - np.arccos(np.minimum(1, theta2))
    else:
       theta2 = np.pi - np.arccos(np.maximum(-1, theta2))

    beta1 = (link2**2 + c**2 - link1**2)/(2*link2*c)
    if(beta1 >= 0.54):
       beta1 = np.arccos(np.minimum(1, beta1))
    else:
       beta1 = np.arccos(np.maximum(-1, beta1))
    beta2 = np.arctan(b/z)

    theta3 = beta1 + beta2 + 1.5708 - np.pi

    servo1 = theta1
    servo2 = -theta2
    servo3 = theta3

    print("Servo1\t: ",np.rad2deg(servo1))
    print("Servo2\t: ",np.rad2deg(servo2))
    print("Servo3\t: ",np.rad2deg(servo3))

    # plot1.figure(figsize=(6, 6))
    plot1.plot([0, link1*np.cos(servo1)], [0, link1*np.sin(servo1)], label='upper_arm', marker='.')

    plot1.plot( [link1*np.cos(servo1), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2)], 
            [link1*np.sin(servo1), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2)], 
            label='lower_arm', marker='.')
    plot1.plot([link1*np.cos(servo1) + link2*np.cos(servo1 + servo2), link1*np.cos(servo1) + link2*np.cos(servo1 + servo2) + link3*np.cos(servo1+servo2+servo3)], 
            [link1*np.sin(servo1) + link2*np.sin(servo1 + servo2), link1*np.sin(servo1) + link2*np.sin(servo1 + servo2) + link3*np.sin(servo1+servo2+servo3)], 
            label='wrist', marker='.')
    plot1.grid(True)
    plot1.legend()
    plot1.set_xlim(-50, 50)
    plot1.set_ylim(-50, 50) 

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    output = FigureCanvasTkAgg(fig, master = canvas)
    output.draw()

    # placing the canvas on the Tkinter window 
    output.get_tk_widget().pack()


# the main Tkinter window 
window = Tk() 

output = None
fig = None

# setting the title 
window.title('Inverse Kinematics Simulation') 

# dimensions of the main window 
window.geometry("700x700") 

canvas = Canvas(window, width=500, height=500, bg='white') 
canvas.pack()

# button that displays the plot 
plot_button = Button(master = window, command = plot, height = 2, width = 10, text = "START") 

up_button = Button(master = window, command = up, height = 2, width = 10, text = "UP", background = "black", fg='white')
down_button = Button(master = window, command = down, height = 2, width = 10, text = "DOWN", background = "black",fg='white')
left_button = Button(master = window, command = left, height = 2, width = 10, text = "LEFT", background = "black",fg='white')
right_button = Button(master = window, command = right, height = 2, width = 10, text = "RIGHT", background = "black",fg='white')

# place the button 
plot_button.pack() 


# run the gui 
window.mainloop()