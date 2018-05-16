from scipy import *
from pylab import *
from sympy import *
from numpy import *


"""
Takes two functions containing variables x, y and computes Newton's method.
"""

# allows variables x and y to be inputs
x, y = symbols('x, y', real=True)


class fractal2D:
    def __init__(self, f1, f2, f1dx, f1dy, f2dx, f2dy, tol, z):
        self.f1 = f1
        self.f2 = f2
        self.tol = tol
        self.z=z
        self.f1dx = f1dx
        self.f1dy = f1dy
        self.f2dx = f2dx
        self.f2dy = f2dy

    # prints the two functions in the form of a Matrix
    def __repr__(self):
        return 'Matrix([[{}], [{}]])'.format(self.f1, self.f2)

    # implements Newton's method
    def newton(self, initial):
        """
        initial should be in the form [x0, y0]
        """
        v = array(initial)
        for i in range(20):
            # used for comparison
            vold = v
            x, y = v[0], v[1]
            # computes Jacobian matrix at a given point
            J = array([[self.f1dx(x,y), self.f1dy(x,y)],
                    [self.f2dx(x,y), self.f2dy(x,y)]])
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
            conv=([10,10],20)
        return conv

    # implements simplified Newton's method
    def simplifiednewton(self, initial):
        """
        initial should be in the form [x0, y0]
        """
        v = array(initial)
        x, y = v[0], v[1]
        # computes Jacobian matrix at a given point
        J = array([[self.f1dx(x,y), self.f1dy(x,y)],
                   [self.f2dx(x,y), self.f2dy(x,y)]])
        invert = inv(J)
        for i in range(20):
            # used for comparison
            vold = v
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
            conv=([10,10],20)
        return conv
        
    def zeroes(self, initial, simplified):
        
        """
        Takes two values. An initial guess in the shape [x0,y0] and a boolean.
        The boolean determines wheter the simplified method should be used or not.
        If the zero value already is in the list it returns the index where it is.
        Otherwise it appends the zero to the list and returns the index where 
        the zero is placed. If the list is empty it appends the zero and returns 
        index 0. If the newton method doesn't detect convergence it returns the 
        index 10.
        """
    
        if simplified==False:
            u=self.newton(initial)[:-1]
            u1=u[0][0]
            u2=u[0][1]
            if u1==10 and u2==10:
                return 10
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
          
        if simplified==True:
            u=self.simplifiednewton(initial)[:-1]
            print(u)
            u1=u[0][0]
            u2=u[0][1]
            if u1==10 and u2==10:
                return 10
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
        
    
    def plot1(self, N, a, b, c, d, simplified):
        
        """
        Takes two intervals, a step size and a boolean  value. The intervals
        determine the initival values of the newton method and the step size how 
        many points the grid will be. The grid contains N*N points. The boolean
        if true makes so that the plot method uses the simplified newtonmethod 
        and false the regular newtonmethod. It plots the index of where the zero 
        is found in red, green, blue and black.
        """
    
        X, Y = meshgrid(linspace(a,b+1, num=N), linspace(c, d+1, num=N), indexing='ij')
        A=[]
        if simplified==False:
            for i in range(N):
                for j in range(N):
                    p=array([X[i,j],Y[i,j]])
                    A.append(self.zeroes(p, False))
            A=reshape(array(A), (N,N))


        if simplified==True:
            for i in range(N):
                for j in range(N):
                    p=array([X[i,j],Y[i,j]])
                    A.append(self.zeroes(p, True))
            A=reshape(array(A), (N,N))
        
        print(A)
        colors=matplotlib.colors.ListedColormap(['salmon', 'darkolivegreen', 'skyblue','black'])
        bounds=[0,1,2,3,10]
        norm=matplotlib.colors.BoundaryNorm(bounds,colors.N)
        return pcolormesh(A, cmap=colors,norm=norm), colorbar(), savefig('Fractal.png')

### TESTS ###
F = fractal2D(lambda x,y: x**3-3*x*y**2-1, lambda x,y: 3*x**2*y-y**3,
              lambda x,y: 3*x**2 - 3*y**2, lambda x,y: -6*x*y,
              lambda x,y: 6*x*y, lambda x,y: 3*x**2 - 3*y**2, 1.e-8, z=[])

F2=fractal2D(lambda x,y: x**8-28*x**6*y**2+70*x**4*y**4+15*x**4-28*x**2*y**6-90*x**2*y**2+y**8+15*y**4-16,
             lambda x,y: 8*x**7*y-56*x**5*y**3+56*x**3*y**5+60*x**3*y-8*x*y**7-60*x*y**3,
             lambda x,y: 4*x*(2*x**6-42*x**4*y**2+5*x**2*(14*y**4+3)-y**2*(14*y**4+45)),
             lambda x,y: 4*y*(-14*x**6+70*x**4*y**2-3*x**2*(14*y**4+15)+y**2*(2*y**4+15)),
             lambda x,y: 4*y*(14*x**6-70*x**4*y**2+x**2*(42*y**4+45)-y**2*(2*y**4+15)),
             lambda x,y: 4*x*(2*x**6-42*x**4*y**2+5*x**2*(14*y**4+3)-y**2*(14*y**4+45)),
             1.e-8, z=[])
F.plot1(50,-10,10,-10,10, False)
#F2.plot1(1000,-10,10,-10,10,False)

