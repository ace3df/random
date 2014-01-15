# >2014 importing in 1 line
import Tkinter as tk
from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image
import re
import random
import os

def THETIMERERRZRZR():
    if (gogo):
        global timer
        # add 1 to millisecond. 2 becuase Python LAAAAAAAAAAAAAAAAAAAG
        timer[2] += 2
        # second
        if timer[2] >= 100:
            timer[2] = 0
            timer[1] += 1
        # min
        if timer[1] >= 60:
            timer[0] += 1
            timer[1] = 0
        # hour
        if timer[0] >= 60:
            timer[3] += 1
            timer[0] = 0
        timeString = pattern.format(timer[0], timer[1], timer[2], timer[3])
        timeText.configure(text=timeString)
    # loop da loop
    root.after(10, THETIMERERRZRZR)

def start():
    global gogo
    if timeText["foreground"] == "blue":
    	global timer
    	timer = [0, 0, 0, 0]
    	timeText.configure(text='00:00:00.00', foreground="black")
    	gogo = True
    else:
	    gogo = True
	    timeText.configure(foreground="black")

def pause():
    global gogo
    gogo = False
    timeText.configure(foreground="darkred")

def stop():
    global gogo
    gogo = False
    timeText.configure(foreground="blue")
	# OH BOYYYYY
    CurrentTime = timeText["text"]
    CurrentTime = CurrentTime[:-3]
    CurrentTime = CurrentTime.replace(":","")
	# PB
    PersonalB = var.get()
    PersonalB = PersonalB[:-3]
    PersonalB = PersonalB.replace(":","")
    print int(CurrentTime)
    print int(PersonalB)
    if CurrentTime > PersonalB:
        timeDif = abs(int(CurrentTime) - int(PersonalB))
        tkMessageBox.showinfo("Yaoi PB", "Good job by smashing your PB take a Yaoi image")
        ran = random.randint(0,5)
        print ran
        img = str(ran)+'.jpg'
        try:
            os.system('start yaoipics/' + img)
        except:
            print "Image couldn't open fuck me sideways python is shit"
    else:
        tkMessageBox.showinfo("no yaoi", "ur shit m8 no yaoi for you")

def reset():
    global timer
    timer = [0, 0, 0, 0]
    timeText.configure(text='00:00:00.00', foreground="black")

def dead():
    root.destroy()

gogo = False

root = tk.Tk()
root.wm_title('Yaoi Timer')

# hour, min, sec, mil
timer = [0, 0, 0, 0]
# format the timer 
pattern = '{3:02d}:{0:02d}:{1:02d}.{2:02d}'

# put image background naruto desu
imag = tk.PhotoImage(file="yaoipics/rsz_1rsz_img.gif")
w = imag.width()
h = imag.height()

panel = tk.Label(root, image=imag)
panel.grid(rowspan=5,columnspan=6)

# button city
timeText = tk.Label(root, text="00:00:00.00", font=("232MKSD", 50))
timeText.grid(row=0,columnspan=6)

startButton = tk.Button(root, text='Start', width=10, height=1, command=start)
startButton.grid(row=1,column=1)

stoptButton = tk.Button(root, text='Stop', width=10, height=1, command=stop)
stoptButton.grid(row=1,column=2)

pauseButton = tk.Button(root, text='Pause', width=10, height=1, command=pause)
pauseButton.grid(row=1,column=3)

resetButton = tk.Button(root, text='Reset', width=10, height=1, command=reset)
resetButton.grid(row=1,column=4)

quitButton = tk.Button(root, text='Quit', width=10, height=1, command=dead)
quitButton.grid(row=1,column=5)

pbtext = tk.Label(root, text="PB: ", font=("232MKSD", 10))
pbtext.grid(row=2,column=2)

# vars in text is dumb gui more like shitUI hahahahahauihfisuahfoisa
var = StringVar()
var.set('00:00:00.00')
pb = tk.Entry(root, textvariable=var)
pb.config(width=10)
pb.grid(row=2,column=3)

# save the panel's image from 'garbage collection' shit
panel.image = imag

# loop da loop
THETIMERERRZRZR()
root.mainloop()
