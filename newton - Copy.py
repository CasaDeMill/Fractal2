from scipy import *
from pylab import *
from numpy import *
from matplotlib.animation import *
import time


"""
Takes two functions containing variables x, y and computes Newton's method.
"""


class fractal2D:
    def __init__(self, f1, f2, f1dx, f1dy, f2dx, f2dy, tol=1.e-8, z=[]):
        self.f1 = f1
        self.f2 = f2
        self.f1dx = f1dx
        self.f1dy = f1dy
        self.f2dx = f2dx
        self.f2dy = f2dy
        self.tol = tol
        self.z = z

    # prints the two functions in the form of a Matrix
    def __repr__(self):
        return 'matrix([[{}], [{}]])'.format(self.f1, self.f2)
    def numdif(self, initial, h):
        v = array(initial)
        x, y = v[0], v[1]
        Jh = array([[self.f1(x+h,y), self.f1(x,y+h)],
                    [self.f2(x+h,y), self.f2(x,y+h)]])
        J = array([[self.f1(x,y), self.f1(x,y)],
                    [self.f2(x,y), self.f2(x,y)]])
        dif = (Jh-J)/h
        return dif
    # implements Newton's method
    def newton(self, initial,simplified, exact, h):
        if simplified == False:
            """
            initial should be in the form [x0, y0]
            """
            iterations=0
            v = array(initial)
            for i in range(200):
                iterations=iterations+1
                # used for comparison
                vold = v
                x, y = v[0], v[1]
                # computes Jacobian matrix at a given point
                if exact:
                    J = array([[self.f1dx(x,y), self.f1dy(x,y)],
                           [self.f2dx(x,y), self.f2dy(x,y)]])
                else:
                    J = self.numdif(v,h)
                invert = inv(J)
                # computes function matrix at a given point
                F = array([self.f1(x,y), self.f2(x,y)])
                # implements Newton's method
                v = v - invert.dot(F)
                # tolerance check
                if abs(v[0]-vold[0]) < self.tol:
                    if abs(v[1]-vold[1]) < self.tol:
                        conv = ([v[0], v[1]], i)
                        break
            else:
                conv = ((5,5),iterations)
            return conv
        else:
            """
            initial should be in the form [x0, y0]
            """
            iterations=0
            v = array(initial)
            x, y = v[0], v[1]
            # computes Jacobian matrix at a given point
            if exact:
                J = array([[self.f1dx(x,y), self.f1dy(x,y)],
                           [self.f2dx(x,y), self.f2dy(x,y)]])
            else:
                J = self.numdif(v,h)
            invert = inv(J)
            for i in range(200):
                iterations=iterations+1
                # used for comparison
                vold = v
                x, y = v[0], v[1]
                # computes function matrix at a given point
                F = array([self.f1(x,y), self.f2(x,y)])
                # implements Newton's method
                v = v - invert.dot(F)
                # tolerance check
                if abs(v[0]-vold[0]) < self.tol:
                    if abs(v[1]-vold[1]) < self.tol:
                        conv = ([v[0], v[1]], i)
                        break
            else:
                conv = ((5,5),iterations)
            return conv
        
    def zeroes(self, initial, simplified, exact, h):
        
        """
        Takes two values. An initial guess in the shape [x0,y0] and a boolean.
        The boolean determines wheter the simplified method should be used or not.
        If the zero value already is in the list it returns the index where it is.
        Otherwise it appends the zero to the list and returns the index where 
        the zero is placed. If the list is empty it appends the zero and returns 
        index 0. If the newton method doesn't detect convergence it returns the 
        index 10.
        """
    
        u=self.newton(initial, simplified, exact, h)[:-1]
        u1=u[0][0]
        u2=u[0][1]
        if u1==5 and u2==5:
            return 5
        if not self.z:
            self.z.append(u)
            return 0
        else:
            for n in range(len(self.z)):
                if abs(self.z[n][0][0]-u1) > self.tol and abs(self.z[n][0][1]-u2) > self.tol:
                    self.z.append(u)
                    return n+1
                else:
                    if abs(self.z[n][0][0]-u1) < self.tol and abs(self.z[n][0][1]-u2) < self.tol:
                        return n
        
    
    def plot1(self, N, a, b, c, d, simplified, exact, h):
        
        """
        Takes two intervals, a step size and a boolean  value. The intervals
        determine the initival values of the newton method and the step size how 
        many points the grid will be. The grid contains N*N points. The boolean
        if true makes so that the plot method uses the simplified newtonmethod 
        and false the regular newtonmethod. It plots the index of where the zero 
        is found in red, green, blue and black.
        """
    
        X, Y = meshgrid(linspace(a,b, num=N), linspace(c, d, num=N), indexing='ij')
        A=[]
        for i in range(N):
            for j in range(N):
                p=array([X[i,j],Y[i,j]])
                A.append(self.zeroes(p, simplified, exact, h))
        A=reshape(array(A), (N,N))

        
        
        colors=matplotlib.colors.ListedColormap(['red', 'green', 'blue','black'])
        bounds=[0,1,2,3,10]
        norm=matplotlib.colors.BoundaryNorm(bounds,colors.N)
        axis([X.min(),X.max(),Y.min(),Y.max()])
        return pcolormesh(X,Y,A, cmap=colors,norm=norm), colorbar(), savefig('Fractal.png')
        
    def IterPlot(self, N, a,b,c,d,simplified, exact, h):
        xmin= a; xmax= b; dx = (xmax-xmin)/N
        ymin= c; ymax= d; dy= (ymax-ymin)/N
        x,y = meshgrid(linspace(xmin,xmax,N),linspace(ymin,ymax,N))
        I=empty((N,N))
        for r in range(N):
            for k in range(N):
                I[r,k]=self.newton((xmin+k*dx+0.0001,ymin+r*dy+0.0001), simplified, exact, h)[1]
        axis([x.min(),x.max(),y.min(),y.max()])
        return pcolormesh(x,y,I,cmap='rainbow'),colorbar(cmap='rainbow')
        
    def animation(self, N, a,b,c,d, simplified, exact, h):
        
        X, Y = meshgrid(linspace(a,b+1, num=N), linspace(c, d+1, num=N), indexing='ij')
        A=[]
        for i in range(N):
            for j in range(N):
                p=array([X[i,j],Y[i,j]])
                A.append(5*self.zeroes(p, simplified, exact, h))
        A=reshape(array(A), (N,N))
        
        xmin= a; xmax= b; dx = (xmax-xmin)/N
        ymin= c; ymax= d; dy= (ymax-ymin)/N
        x,y = meshgrid(arange(xmin,xmax,dx)-dx/2.,arange(ymin,ymax,dy)-dy/2.)
        I=empty((N,N))
        for r in range(N):
            for k in range(N):
                p=array([x[r,k],y[r,k]])
                I[r,k]=self.newton((xmin+k*dx+0.0001,ymin+r*dy+0.0001), simplified, exact, h)[1]
        B=I
        
        self.fig = figure()
        self.ax = self.fig.add_subplot(1,1,1)
        
        def update(i): #funktion som upprepas varje gång processorn "tickar", med ökande i
            C = (A*(1+sin(i*pi/16)) + B*(1-sin(i*pi/16)))/2
            pcolor(C)
            time.sleep(0.25)
            
        self.anim = FuncAnimation(self.fig, update)
        
        
        
#F = fractal2D(lambda x,y: x**3-3*x*y**2-1, lambda x,y: 3*x**2*y-y**3,
#              lambda x,y: 3*x**2 - 3*y**2, lambda x,y: -6*x*y,
#              lambda x,y: 6*x*y, lambda x,y: 3*x**2 - 3*y**2, 1.e-8, z=[])
#F.animation(40,-10,10,-10,10, False)