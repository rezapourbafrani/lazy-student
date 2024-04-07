import tkinter as tk
from datetime import datetime
import requests
import threading
from itertools import count
from tkinter import *
from PIL import ImageTk, Image

clock_webservice_address = "https://api.codebazan.ir/time-date/?td=time"


# ------------------------------------------------- digit clock
class Clock:
    def __init__(self, window, lable):
        self.lable = lable
        self.window = window
        self.label = Label(text="")
        # self.label.pack()
        self.update_clock()
        # clock = threading.Thread(target=self.update_clock, args=())
        # clock.start()

    def update_clock(self):
        now = datetime.now()
        now = now.strftime("%H:%M:%S")
        # current_time = requests.get(clock_webservice_address).text
        self.lable.configure(text=now)
        self.window.after(1000, self.update_clock)


# --------------------------------------------------- Play Gif
class ImageLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


# --------------------------------------------------- Bottom Windows
def down_window(width, height, window):
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    # print("x is %d and y is %d" % (ws, hs))
    # calculate x and y coordinates for the Tk root window
    x = (ws) - width
    y = hs - height - 50
    # print("x is %d and y is %d" % (x, y))
    # set the dimensions of the screen
    # and where it is placed
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


# --------------------------------------------------- Center Windows
def center_window(width, height, window):
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    # print("x is %d and y is %d" % (ws, hs))

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (width / 2)
    y = (hs / 2) - (height / 2)
    # print("x is %d and y is %d"%(x,y))

    # set the dimensions of the screen
    # and where it is placed
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

# top.after(5,restart())
