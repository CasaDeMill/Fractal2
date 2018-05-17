from numpy import *
import os
import sys
from tkinter import *
from matplotlib.animation import *
import NEWTON


    
class App(Tk):
    
    def apply(self):
         
         #self.Fractal = newton.fractal2D(self.func1, self.func2, self.f1dx, \
         #self.f1dy, self.f2dx, self.f2dy, self.tol)
         self.Fractal = newton.fractal2D(lambda x,y: eval(self.f1.get()), lambda x,y: eval(self.f2.get()),
                                         lambda x,y: eval(self.f1x.get()), lambda x,y: eval(self.f1y.get()),
                                         lambda x,y: eval(self.f2x.get()), lambda x,y: eval(self.f2y.get()), eval(self.Tolerance.get()), z=[])
                                     
            
        
    def plot1(self):
        a,b = eval(self.XInterval.get())
        c,d = eval(self.YInterval.get())
        N = eval(self.Ns.get())
        simplified = self.A.get()
        exact = self.B.get()
        h = eval(self.StepSize.get())
        self.Fractal.plot1(N, a,b,c,d, simplified, exact, h)
        
    def plot2(self):
        a,b = eval(self.XInterval.get())
        c,d = eval(self.YInterval.get())
        N = eval(self.Ns.get())
        simplified = self.A.get()
        exact = self.B.get()
        h = eval(self.StepSize.get())
        self.Fractal.IterPlot(N, a,b,c,d, simplified, exact, h)
        
    def animate(self):
        a,b = eval(self.XInterval.get())
        c,d = eval(self.YInterval.get())
        N = eval(self.Ns.get())
        simplified = self.A.get()
        exact = self.B.get()
        h = eval(self.StepSize.get())
        self.Fractal.animation(N, a,b,c,d, simplified, exact, h)

    
    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
    
        self.fg = "light blue"
            
        self.configure(background="indigo")
        self.geometry("420x230")
        
        self.A= IntVar()
        self.SimpNew=Checkbutton(self, text="Simplified Newton Method", \
        variable = self.A, onvalue=1, offvalue=0,bg="indigo", fg=self.fg)
        self.B=IntVar()
        self.ExactDer=Checkbutton(self, text="Exact Derivative", \
        variable = self.B, \
        onvalue=1, offvalue=0,bg="indigo", fg=self.fg)

        self.C=StringVar()
        self.f1=Entry(self, textvariable=self.C)
        self.D=StringVar()
        self.f2=Entry(self, textvariable=self.D)
        self.I=StringVar()
        self.StepSize=Entry(self, textvariable=self.I)
        self.J=StringVar()
        self.Tolerance=Entry(self, textvariable=self.J)
        
        self.K = StringVar()
        self.XInterval = Entry(self, textvariable = self.K)
        self.LXI = Label(self, text = "X-interval",bg="indigo", fg=self.fg)
        self.L = StringVar()
        self.YInterval = Entry(self, textvariable = self.L)
        self.LYI = Label(self, text = "Y-interval",bg="indigo", fg=self.fg)
        self.M = StringVar()
        self.Ns = Entry(self, textvariable = self.M)
        self.LNs = Label(self, text = "N",bg="indigo", fg=self.fg)
        
        self.O = StringVar()
        self.f1x = Entry(self, textvariable = self.O)
        self.Lf1x= Label(self, text = "df1/dx=",bg="indigo", fg=self.fg)
        self.P = StringVar()
        self.f1y = Entry(self, textvariable = self.P)
        self.Lf1y= Label(self, text = "df1/dy=",bg="indigo", fg=self.fg)
        self.Q = StringVar()
        self.f2x = Entry(self, textvariable = self.Q)
        self.Lf2x= Label(self, text = "df2/dx=",bg="indigo", fg=self.fg)
        self.R = StringVar()
        self.f2y = Entry(self, textvariable = self.R)
        self.Lf2y= Label(self, text = "df1/dx=",bg="indigo", fg=self.fg)
       
            
        self.Apply=Button(self, text="Apply", font=", 9",bg="yellow",fg="black", command = self.apply) 
        self.Plot1=Button(self, text="Plot 1", command = self.plot1,bg="yellow", fg="black")
        self.Plot2=Button(self, text="Plot 2", command = self.plot2,bg="yellow", fg="black")
        self.Animation= Button(self, text="Animation", command = self.animate, bg="yellow",fg="black")

        self.Lf1=Label(self, text="f1(x,y)=",bg="indigo", fg=self.fg)
        self.Lf2=Label(self, text="f2(x,y)=",bg="indigo", fg=self.fg)
        self.LStepSize=Label(self, text="Stepsize=",bg="indigo", fg=self.fg)
        self.LTolerance=Label(self, text="Tolerance=",bg="indigo", fg=self.fg)


        self.SimpNew.grid(row = 0, column = 1, sticky="e")
        self.ExactDer.grid(column=3,row=0)
        
        self.f1.grid(row = 1, column = 1)
        self.Lf1.grid(row = 1, column = 0)
        self.f2.grid(row = 3, column = 1)
        self.Lf2.grid(row = 3, column = 0)
        
        self.Lf1x.grid(row = 1, column = 2)
        self.f1x.grid(row = 1, column = 3)
        self.Lf1y.grid(row = 2, column = 2)
        self.f1y.grid(row = 2, column = 3)
        self.Lf2x.grid(row = 3, column = 2)
        self.f2x.grid(row = 3, column = 3)
        self.Lf2y.grid(row = 4, column = 2)
        self.f2y.grid(row = 4, column = 3)
        
        self.LXI.grid(row = 5, column = 0)
        self.XInterval.grid(row = 5, column =1)
        self.LYI.grid(row = 5, column = 2)
        self.YInterval.grid(row = 5, column = 3)
        self.LNs.grid(row = 6, column = 0)
        self.Ns.grid(row = 6, column = 1)
        
        self.StepSize.grid(row = 7, column = 1)
        self.LStepSize.grid(row = 7, column =0)
        self.Tolerance.grid(row = 6, column = 3)
        self.LTolerance.grid(row=6, column = 2)

        self.Apply.place(x=69,y=200)
        self.Plot1.place(x=109,y=200)
        self.Plot2.place(x=150,y=200)
        self.Animation.place(x=191,y=200)
        



app = App()
app.mainloop()