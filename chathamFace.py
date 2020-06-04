from Tkinter import *
import Tkinter as tk
import math
from time import *
import numpy as np
import sys
import threading
import datetime
import time
from freenect import sync_get_depth as get_depth

#set size for canvas
WIDTH=800
HEIGHT=400

#initialize the face
class RobotGUI():
    def __init__(self):
        print "running UI"
        self.state = "blink"
        self.pupilpos = .5
        self.newpupilpos = .5
        self.eyedirection = "down"
        self.root = Tk(className="Robot UI")
        self.root.minsize(width=WIDTH, height=HEIGHT)
        #the background is the chatham purple
        self.root.tk_setPalette(background='#4E2A6E')
        pad=3
        #this code allows you to use the Escape key to switch between fullscreen and partial screen
        self._geom='200x200+0+0'
        self.root.geometry("{0}x{1}+0+0".format(
            self.root.winfo_screenwidth()-pad, self.root.winfo_screenheight()-pad))
        self.root.bind('<Escape>',self.toggle_geom) 

        print "done geometry"
        #set up the face, background is the Chatham purple
        self.facecanvas = Canvas(self.root, width=800, height=400, bg='#4E2A6E')
        self.lefteye = self.facecanvas.create_oval(450,190,600,375,fill="white",outline="#4E2A6E")
        self.leftpupil = self.facecanvas.create_oval(475,250,575,350,fill="black")
        self.righteye = self.facecanvas.create_oval(700,190,850,375,fill="white",outline="#4E2A6E")
        self.rightpupil = self.facecanvas.create_oval(725,250,825,350,fill="black")
        self.uppersmile = self.facecanvas.create_arc(450,350,850,600,fill="black",start=200,extent=140,width=10,style=ARC)
        self.nose = self.facecanvas.create_arc(600,375,700,475,fill="black",start=90,extent=130,width=5,style=ARC)
        #eyelids that will move over the eyes to blink/sleep
        self.lefteyelid = self.facecanvas.create_oval(450,5,600,190,fill='#4E2A6E',outline="#4E2A6E")
        self.righteyelid = self.facecanvas.create_oval(700,5,850,190,fill='#4E2A6E',outline="#4E2A6E")
        #eyebrows
        self.lefteyebrows = self.facecanvas.create_arc(450,100,600,175,fill="black",start=20,extent=140,width=7,style=ARC)
        self.righteyebrows = self.facecanvas.create_arc(850,100,700,175,fill="black",start=20,extent=140,width=7,style=ARC)
        #Zzz
        self.rightcloselid = self.facecanvas.create_arc(700,225,850,375,fill="black",start=200,extent=140,width=7,style=ARC, state=tk.HIDDEN)
        self.leftcloselid = self.facecanvas.create_arc(450,225,600,375,fill="black",start=200,extent=140,width=7,style=ARC, state=tk.HIDDEN)
        self.Z1 = self.facecanvas.create_text(1050,100,text="Z",state=tk.HIDDEN,font=("Comic Sans MS",120, 'bold'))
        self.Z2 = self.facecanvas.create_text(970,185,text="Z",state=tk.HIDDEN,font=("Comic Sans MS",90, 'bold'))
        self.Z3 = self.facecanvas.create_text(900,250,text="Z",state=tk.HIDDEN,font=("Comic Sans MS",75, 'bold'))
        #pack canvas
        self.facecanvas.pack(fill="both",expand=YES)

        print "done making face"
        #Call Animation
        #self.root.after(1000, self.blink)
        #self.root.after(1000, self.sleep)

        #this code sets two functions moveEyeballsLeft and moveEyeballsRight to move the eyes
       # self.root.bind('<Left>',self.moveEyeballsLeftEvent)
       # self.root.bind('<Right>',self.moveEyeballsRightEvent)
    
    #move the eyeballs left until it reaches the edge of the eyes (magic number 460)
    #def moveEyeballsLeftEvent(self,event):
     #   self.moveEyeballsLeft()
        
  #  def moveEyeballsLeft(self):
   #     if self.facecanvas.coords(self.leftpupil)[0] > 450:
    #        self.facecanvas.move(self.leftpupil,-5,0)
     #       self.facecanvas.move(self.rightpupil,-5,0)

    #move the eyeballs right until it reaches the edge of the eyes (magic number 490)
 #   def moveEyeballsRightEvent(self,event):
  #      self.moveEyeballsRight()

  #  def moveEyeballsRight(self):
   #     if self.facecanvas.coords(self.leftpupil)[0] < 500:
    #        self.facecanvas.move(self.leftpupil,5,0)
     #       self.facecanvas.move(self.rightpupil,5,0)

    def doblinkstep(self):
        if self.eyedirection == "down":
            self.facecanvas.move(self.lefteyelid,0,5)#5 pixels at a time
            self.facecanvas.move(self.righteyelid,0,5)
        else:
            self.facecanvas.move(self.lefteyelid,0,-5)#5 pixels at a time
            self.facecanvas.move(self.righteyelid,0,-5)
        self.facecanvas.update()
        leftlidpos = self.facecanvas.coords(self.lefteyelid)
        if leftlidpos[1] >= 190:
            self.eyedirection = "up"
        if leftlidpos[1] <= 5:
            self.eyedirection = "down"
        if leftlidpos[1] <= 5:
            return "done"
        else:
            return direction

    def doeyeclosestep(self):
        leftlidpos = self.facecanvas.coords(self.lefteyelid)
        if leftlidpos[1] >= 190:
            return "done"
        self.facecanvas.move(self.lefteyelid,0,5)#5 pixels at a time
        self.facecanvas.move(self.righteyelid,0,5)
        self.facecanvas.update()
        return "down"

    def doeyeopenstep(self):
        leftlidpos = self.facecanvas.coords(self.lefteyelid)
        if leftlidpos[1] <= 5:
            return "done"
        self.facecanvas.move(self.lefteyelid,0,-5)#5 pixels at a time
        self.facecanvas.move(self.righteyelid,0,-5)
        self.facecanvas.update()
        return "up"
        
    def doeyelid(self):
        self.facecanvas.itemconfigure(self.rightcloselid,state=tk.NORMAL)
        self.facecanvas.itemconfigure(self.leftcloselid,state=tk.NORMAL)

    def doeyelidclear(self):
        self.facecanvas.itemconfigure(self.rightcloselid,state=tk.HIDDEN)
        self.facecanvas.itemconfigure(self.leftcloselid,state=tk.HIDDEN)

    def pupilposition(self):
        #print self.pupilpos
        if self.pupilpos<.09:
            self.facecanvas.coords(self.leftpupil, 450, 250, 550, 350)
            self.facecanvas.coords(self.rightpupil, 700, 250, 800, 350)
        elif self.pupilpos<.18:
            self.facecanvas.coords(self.leftpupil, 455, 250, 555, 350)
            self.facecanvas.coords(self.rightpupil, 705, 250, 805, 350)
        elif self.pupilpos<.27:
            self.facecanvas.coords(self.leftpupil, 460, 250, 560, 350)
            self.facecanvas.coords(self.rightpupil, 710, 250, 810, 350)
        elif self.pupilpos<.36:
            self.facecanvas.coords(self.leftpupil, 465, 250, 565, 350)
            self.facecanvas.coords(self.rightpupil, 715, 250, 815, 350)
        elif self.pupilpos<.45:
            self.facecanvas.coords(self.leftpupil, 470, 250, 570, 350)
            self.facecanvas.coords(self.rightpupil, 720, 250, 820, 350)
        elif self.pupilpos<.55:
            self.facecanvas.coords(self.leftpupil, 475, 250, 575, 350)
            self.facecanvas.coords(self.rightpupil, 725, 250, 825, 350)
        elif self.pupilpos<.64:
            self.facecanvas.coords(self.leftpupil, 480, 250, 580, 350)
            self.facecanvas.coords(self.rightpupil, 730, 250, 830, 350)
        elif self.pupilpos<.73:
            self.facecanvas.coords(self.leftpupil, 485, 250, 585, 350)
            self.facecanvas.coords(self.rightpupil, 735, 250, 835, 350)
        elif self.pupilpos<.82:
            self.facecanvas.coords(self.leftpupil, 490, 250, 590, 350)
            self.face.canvas.coords(self.rightpupil, 740, 250, 840, 350)
        elif self.pupilpos<.91:
            self.facecanvas.coords(self.leftpupil, 495, 250, 595, 350)
            self.facecanvas.coords(self.rightpupil, 745, 250, 845, 350)
        elif self.pupilpos<1:
            self.facecanvas.coords(self.leftpupil, 450, 250, 600, 350)
            self.facecanvas.coords(self.rightpupil, 750, 250, 850, 350)


    #zzz functions
    def z3(self):
        self.facecanvas.itemconfigure(self.Z3,state=tk.NORMAL)
        #self.root.after(1000, self.z2)
            
    def z2(self):
        self.facecanvas.itemconfigure(self.Z2,state=tk.NORMAL)
        #self.root.after(1000, self.z1)
            
    def z1(self):
        self.facecanvas.itemconfigure(self.Z1,state=tk.NORMAL)
        #self.root.after(2000, self.zclear)
        
    def zclear(self):
        self.facecanvas.itemconfigure(self.Z3,state=tk.HIDDEN)
        self.facecanvas.itemconfigure(self.Z2,state=tk.HIDDEN)
        self.facecanvas.itemconfigure(self.Z1,state=tk.HIDDEN)
        #self.root.after(1000, self.z3)
        self.facecanvas.update()  
            
    #the function that gets called when you press escape
    def toggle_geom(self,event):
        geom=self.root.winfo_geometry()
        print(geom,self._geom)
        self.root.geometry(self._geom)
        self._geom=geom
        self.state = "quit"


def make_gamma():
    """
    Create a gamma table
    """
    num_pix = 2048 # there's 2048 different possible depth values
    npf = float(num_pix)
    _gamma = np.empty((num_pix, 3), dtype=np.uint16)
    for i in xrange(num_pix):
        v = i / npf
        v = pow(v, 3) * 6
        pval = int(v * 6 * 256)
        lb = pval & 0xff
        pval >>= 8
        if pval == 0:
            a = np.array([255, 255 - lb, 255 - lb], dtype=np.uint8)
        elif pval == 1:
            a = np.array([255, lb, 0], dtype=np.uint8)
        elif pval == 2:
            a = np.array([255 - lb, lb, 0], dtype=np.uint8)
        elif pval == 3:
            a = np.array([255 - lb, 255, 0], dtype=np.uint8)
        elif pval == 4:
            a = np.array([0, 255 - lb, 255], dtype=np.uint8)
        elif pval == 5:
            a = np.array([0, 0, 255 - lb], dtype=np.uint8)
        else:
            a = np.array([0, 0, 0], dtype=np.uint8)

        _gamma[i] = a
    return _gamma


gamma = make_gamma()


def uiloop(ui):
    print "UI"
    oldstate = ui.state
    statetransitiontime = datetime.datetime.now()
    substate = "start"
    while ui.state != quit:
        ui.root.update()
        if oldstate != ui.state:
            print "received "+ui.state
            oldstate = ui.state
            substate = "start"
            statetransitiontime = datetime.datetime.now()
        if oldstate == "blink":
            ui.pupilposition()
            #print ui.pupilpos
            if substate == "blinkingdown":
                s = ui.doeyeclosestep()
                if s == "done":
                    substate = "blinkingup"
            elif substate == "blinkingup":
                s = ui.doeyeopenstep()
                if s == "done":
                    substate = "eyesopen"
                    statetransitiontime = datetime.datetime.now()
            elif substate == "eyesopen" and datetime.datetime.now()-statetransitiontime > datetime.timedelta(seconds=5):
                substate = "blinkingdown"
            elif substate == "start":
                ui.zclear()
                ui.doeyelidclear()
                s = ui.doeyeopenstep()
                if s == "done":
                    substate = "eyesopen"
                    statetransitiontime = datetime.datetime.now()
        if oldstate == "sleep":
            if substate == "start":
                s = ui.doeyeclosestep()
                if s == "done":
                    ui.doeyelid()
                    substate = "eyesclosed"
                    statetransitiontime = datetime.datetime.now()
            elif substate == "eyesclosed" and datetime.datetime.now()-statetransitiontime > datetime.timedelta(seconds=1):
                ui.z3()
                substate = "z3"
                statetransitiontime = datetime.datetime.now()
            elif substate == "z3" and datetime.datetime.now()-statetransitiontime > datetime.timedelta(seconds=1):
                ui.z2()
                substate = "z2"
                statetransitiontime = datetime.datetime.now()
            elif substate == "z2" and datetime.datetime.now()-statetransitiontime > datetime.timedelta(seconds=1):
                ui.z1()
                substate = "z1"
                statetransitiontime = datetime.datetime.now()
            elif substate == "z1" and datetime.datetime.now()-statetransitiontime > datetime.timedelta(seconds=1):
                ui.zclear()
                substate = "eyesclosed"
                statetransitiontime = datetime.datetime.now()


def testloop(ui):
    print "KINECT"
    while ui.state != "quit":
        print "what should the eye state be? (sleep, blink, quit)"
        input = sys.stdin.readline().strip()
        if input == "sleep":
            print "going to sleep"
            ui.state = input
        elif input == "blink":
            print "blinking"
            ui.state = input
        elif input == "quit":
            print "quitting"
            ui.state = input

def kinectloop(ui):
    print "KINECT"
    FPS = 30 # kinect only outputs 30 fps
    disp_size = (640, 480)
#	for k in range(100):
    while ui.state != "quit":
        depth = np.rot90(get_depth()[0])
        #print "depth"
        sys.stdout.flush()
        #pixels = gamma[depth]
        mindepth = 2048
        mini = -1
        minj = -1
        print str(len(depth))
        for i in range(len(depth)):
            for j in range(len(depth[i])):
                if depth[i][j] < mindepth:
                    mindepth = depth[i][j]
                    mini = i
                    minj = j
        sys.stdout.flush()
        if mindepth < 800:
            ui.state="blink"
        else:
            ui.state="sleep"
        percent=mini/640.0
        
        ui.newpupilpos = percent
        print percent
        #based on depth, set ui.state = "blink" or "sleep"
        #call ui.moveEyeballsLeft(), ui.moveEyeballsRight(), or make your own function to move eyes depending on i and j


if __name__ == "__main__":
    #This creates the face
    robotUI = RobotGUI()
    
    #kinectloop(robotUI)
    #run the kinect code in a separate thread
    kinectThread = threading.Thread(target=kinectloop, args=(robotUI,))
    #kinectThread = threading.Thread(target=testloop, args=(robotUI,))
    kinectThread.start()

    #run the UI in this main thread
    uiloop(robotUI)
    
    #when you press escape, the kinect should stop looping
    kinectThread.join()
