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
    def __init__(self, f1, f2, tol, z, L):
        self.f1 = f1
        self.f2 = f2
        self.tol = tol
        self.z=z
        self.L = L
        
    # prints the two functions in the form of a Matrix
    def __repr__(self):
        return 'Matrix([[{}], [{}]])'.format(self.f1, self.f2)

    # implements Newton's method
    def newton(self, initial):
        """
        initial should be in the form [x0, y0]
        """
        # creates a matrix that can be turned into a Jacobian matrix
        F = Matrix([self.f1, self.f2])
        # creates a Jacobian matrix with the two given functions
        J = F.jacobian([x, y])
        # turns initial values into an array
        v = array(initial)
        for i in range(400):
            # used for comparison
            vold = v
            # computes Jacobian matrix at a given point
            compJac = J.subs([(x, v[0]), (y, v[1])])
            invert = compJac**-1
            # implements Newton's method
            v =v - invert.dot(F.subs([(x, v[0]), (y, v[1])]))
            # tolerance check
            if abs(v[0]-vold[0]) < self.tol:
                if abs(v[1]-vold[1]) < self.tol:
                    conv = ([v[0],v[1]],i)
                    break
        else:
            raise Exception('No convergence (yet)')
        return conv

    # implements simplified Newton's method
    def simplifiednewton(self, initial):
        """
        initial should be in the form [x0, y0]
        """
        v = array(initial)
        # creates a matrix that can be turned into a Jacobian matrix
        F = Matrix([self.f1, self.f2])
        # creates a Jacobian matrix with the two given functions
        J = F.jacobian([x, y])
        # computes Jacobian matrix at a given point
        compJac = J.subs([(x, v[0]), (y, v[1])])
        invert = compJac**-1
        # turns initial values into an array
        
        for i in range(400):
            # used for comparison
            vold = v
            # implements Newton's method
            v = v - invert.dot(F.subs([(x, v[0]), (y, v[1])]))
            # tolerance check
            if abs(v[0]-vold[0]) < self.tol:
                if abs(v[1]-vold[1]) < self.tol:
                    conv = ([v[0],v[1]],i)
                    break
        else:
            raise Exception('No convergence (yet)')
        return conv
        
    def zeroes(self, initial, simplified):
        
        if simplified==False:
            u=self.newton(initial)
            u1=u[0][0]
            u2=u[0][1]
            if not self.z:
                self.z.append(u[:-1])
                self.L.append(0)
                return self.L
            else:
                for n in range(len(self.z)):
                    if abs(self.z[n][0][0]-u1) > self.tol and abs(self.z[n][0][1]-u2) > self.tol:
                        self.z.append(u[:-1])
                        self.L.append(n+1)
                        return self.L
                    else:
                        self.L.append(10)
                        return self.L
            
        if simplified==True:
            u=self.simplifiednewton(initial)
            u1=u[0][0]
            u2=u[0][1]
            if not self.z:
                self.z.append(u[:-1])
                return 0
            else:
                for n in range(len(self.z)):
                    if abs(self.z[n][0][0]-u1) > self.tol and abs(self.z[n][0][1]-u2) > self.tol:
                        self.z.append(u[:-1])
                        return n+1
                    else: 
                        return 10
 
       
    
    def plot1(self, N, a, b, c, d, simplified):
        
        
    
        X, Y = meshgrid(linspace(a,b+1, num=N), linspace(c, d+1, num=N), indexing='ij')
        A=[]
        if simplified==False:
            for i in range(N):
                for j in range(N):
                    p=array([X[i,j],Y[i,j]]).T
                    A.append(self.zeroes(p, False))
            A=reshape(array(A[-1]), (N,N))

        if simplified==True:
            for i in range(N):
                for j in range(N):
                    p=array([X[i,j],Y[i,j]]).T
                    A.append(self.zeroes(p, False))
            A=reshape(array(A), (N,N))
        
        colors=matplotlib.colors.ListedColormap(['red', 'green', 'blue'])
        return pcolormesh(A, cmap=colors)

### TESTS ###
F = fractal2D(x**3-3*x*y**2-1, 3*x**2*y-y**3, 1.e-8, z=[], L = [])
F.plot1(10,-10,10,-10,10, False)

