
# coding: utf-8

# # <center>Homework 2  
# ## <center>Martin Lindgren
# ### <center>960613-1416</center>
# 
# <div class="pagebreak"></div>

# In[13]:

#I start with importing two important libraries for this code and make sure that the plots are inline

from scipy import *
from pylab import *
get_ipython().magic('matplotlib inline')


# # The interval class
# ## Task 1-9

# In[14]:

class Interval:
    """
    A class interval that can take either one or two arguments
    these arguments must be real numbers. This interval class has several  arithmetic operations
    and a few other methods. It's represented as a string. 
    """
    def __init__ (self,*args):
        """
        It can either be initialized with one or two arguments. If two arguments, the first one
        gets represented as the left endpoint in the interval and the second the right endpoint.
        If there is only one argument then both both the left and right endpoint gets represented as that number.
        
        It raises errors if the arguments are complex (right now for example strings are possible which would
        create errors further on. This could instead check if it's an int or float and otherweise raise an error.)
        
        It also raises an error if there are anything else than one or two arguments.
        """
        if len(args)==2:
            leftendpoint=args[0]
            rightendpoint=args[1]
        elif len(args)==1:
            leftendpoint, rightendpoint=args[0], args[0]
        else:
            raise TypeError('Interval can only take 1 or 2 arguments')
        if isinstance (leftendpoint, complex):
            raise TypeError('The left endpoint must be a real number')
        if isinstance (rightendpoint, complex):
            raise TypeError('The right endpoint must be a real number')
        self.leftendpoint=leftendpoint
        self.rightendpoint=rightendpoint
    
    def __add__(self, other):
        """
        Adds an interval to either another interval, a float or an int. 
        If it's another interval it adds the left and right endpoints respectively. If it's an int
        it adds the int to both endpoints. If it's a float the same operation as the int occurs, but
        all values are converted to floats. It raises an error if you try to add somethin else than an int, float or 
        interval. It's returned as a new Interval.
        """
        p1, q1 = self.leftendpoint, self.rightendpoint
        if isinstance(other, Interval):
            p2, q2 = other.leftendpoint, other.rightendpoint
        elif isinstance(other, int):
            p2 = other
            q2 = other
        elif isinstance(other, float):
            p2=other
            q2=other
            p1=float(p1)
            q1=float(q1)
        else:
            raise TypeError('An interval can only be added to another interval, int or float')
            
        return Interval(p1+p2,q1+q2)
    
    def __radd__(self, other):
        """
        The same as the add function, but makes sure that an addition can be made in the reversed order.
        """
        return self+other
        
        
    def __sub__(self, other):
        """
        Subtracts an interval with another interval. It raises an error if you try to subtract something else.
        It subtracts the first intervals left endpoint with the seconds right endpoint and subtracts the first intervals 
        right endpoint with the seconds left endpoint. This is returned as a new interval
        """
        p1, q1 = self.leftendpoint, self.rightendpoint
        if isinstance(other, Interval):
            p2, q2 = other.leftendpoint, other.rightendpoint
        else:
            raise TypeError('An interval can only be subtracted of another interval')
            
        return Interval(p1-q2,q1-p2)
        
    def __mul__(self, other):
        """
        Multiplies an interval with another interval. Raises an error if you try to multiply something else.
        It multiplies all combinations of the both intervals right and left endpoints respectively and 
        returns the minimum values as the left endpoint in a new interval and the maximum as the right endpoint.
        """
        p1, q1 = self.leftendpoint, self.rightendpoint
        if isinstance(other, Interval):
            p2, q2 = other.leftendpoint, other.rightendpoint
        else:
            raise TypeError('An interval can only be multiplied to another interval')
            
        return Interval(min(p1*p2,p1*q2,q1*p2,q1*q2),max(p1*p2,p1*q2,q1*p2,q1*q2))
        
        
    def __truediv__(self, other):
        """
        Divides an interval with another interval. Raises an error if you try to divide something else.
        It divides all combinations of the both intervals right and left endpoints respectively and 
        returns the minimum values as the left endpoint in a new interval and the maximum as the right endpoint.
        If an endpoint of the interval which we are trying to divide by is zero it raises an error.
        It also raises an error if the division tends to infinity.
        """
        p1, q1 = self.leftendpoint, self.rightendpoint
        if isinstance(other, Interval):
            p2, q2 = other.leftendpoint, other.rightendpoint
        else:
            raise TypeError('An interval can only be divided by another interval')
        if p2==0:
            raise TypeError('Dividing by zero')
        if q2==0:
            raise TypeError('Dividing by zero')
        if isinf(min(p1/p2,p1/q2,q1/p2,q1/q2)):
            raise TypeError('Division tends to infinity')
        if isinf(max(p1/p2,p1/q2,q1/p2,q1/q2)):
            raise TypeError('Division tends to infinity')
            
        return Interval(min(p1/p2,p1/q2,q1/p2,q1/q2),max(p1/p2,p1/q2,q1/p2,q1/q2))
    
    def __pow__(self, other):
        """
        Raises the endpoints of an interval to a power of an integer. Raises an error if it's not an integer.
        If the left endpoint is the same as the right endpoint, the left endpoint is set to zero. This according
        to homework instructions.
        """
        p1, q1 = self.leftendpoint, self.rightendpoint
        #This for loop does the power calculation. It does so by setting endpoint values to 1 and then 
        #for every loop multiplies it self with the endpoint values we want to raise by a power.
        p2,q2 = 1,1
        if isinstance(other, int):
            for n in range(other):
                p2=p1*p2
                q2=q1*q2
            if p2==q2:
                p2=0
            return Interval(p2,q2)
        else:
            raise TypeError('Can only be raised to the power of an integer')
        
    def __repr__(self):
        """
        Returns a string formated [leftendpoint, rightendpoint] if an Interval is initialized.
        """
        return str([self.leftendpoint, self.rightendpoint])
    def __str__(self):
        """
        Returns the same as __repr__ but this happens when print(Interval) is called. Or Interval.print
        """
        return str([self.leftendpoint, self.rightendpoint])
    
    
    def __contains__(self, other):
        """
        This checks if an int or float is within the interval by seing if it's more or equal to the leftendpoint
        and less or equal to the right endpoint. If it's not an int or float, an error is raised.
        """
        p1, q1 = self.leftendpoint, self.rightendpoint
        if isinstance(other, int) or isinstance(other, float):
            if other >= p1 and other <= q1:
                return True
            else:
                return False
        else:
            raise TypeError('Contain only works for ints and floats')
        


# ## Test of task 3

# In[15]:

Interval(1,2)


# ## Test of task 4

# In[16]:

I1 = Interval(1, 2) # [1, 2] 
I2 = Interval(3, 4) # [3, 4] 
print(I1)
print(I2)
print(I1 + I2) # [4, 6] 
print(I1 - I2) # [-3, -1] 
print(I1 * I2) # [3, 8] 
print(I1 / I2) # [0.25,0.6666666666666666]


# ## Test of task 6

# In[17]:

Interval(1)


# ## Test of task 7

# In[18]:

I3=Interval(2,3)+1
I4=1+Interval(2,3)
I5=1.0+Interval(2,3)
print(I3) #[3,4]
print(I4) #[3,4]
print(I5) #[3.0,4.0]


# ## Test of task 8

# In[19]:

if 8 in Interval(1,10):
    print('It is in the interval')


# ## Test of task 9

# In[20]:

x = Interval(-2,2) # [-2, 2] 
print(x**2) # [0, 4] 
print(x**3) #[-8,8]


# ## Task 10

# In[21]:

#I define two lists of numbers between 0 and 1 with 1000 steps. I also create an empty list called intervals
xl=linspace(0.,1,1000)
xu=linspace(0.,1,1000)+0.5
intervals=[]
#The numbers in the xl list are assigned as left endpoints in intervals which are added to my empty list. 
#xu are assigned as the right endpoints.
for n in range(len(xl)):
    intervals.append(Interval(xl[n],xu[n]))
#The polynomial p(x)=3x^3−2x^2 +5x−1 is evaluated at all intervals in my intervals list 
for n in range(len(intervals)):
    intervals[n]=(Interval(3)*intervals[n]**3)-(Interval(2)*intervals[n]**2)+(Interval(5)*intervals[n])-Interval(1)
#I create two empty lists 
yl=[]
yu=[]
#I append the left endpoints on all my intervals to the yl list and all the right endpoints to my yu list
for n in range(len(intervals)):
    yl.append(intervals[n].leftendpoint)
    yu.append(intervals[n].rightendpoint)
#Both yl and yu are plotted vs. xl.
plot(xl,yl,'b.')
plot(xl,yu,'g.')


# ## Test of task 5 (I do this last because I don't want the error to interupt the rest of my code)

# In[22]:

z=Interval(1,5)/Interval(3,0)
print(z)


# In[ ]:



