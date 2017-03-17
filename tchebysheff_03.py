#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
import sys
import math



def print_done():
    print("[Done]")
    
def print_ok():
    print("[OK]")
    
def print_err():
    print("[error]")

def check_for_root():
	print('Cheking for root...',end="")
	if not os.geteuid() == 0:
	    sys.exit('Script must be run as root')
	print_ok()


def install_binary(b="",dist=""):
	print("binary "+b+" doesn\'t exist")
	if input("Do you want to install it? [y/n] ") == 'y':
		if(dist=="linux"):
			check_for_root()
			if not os.system('apt-get install python3-'+b)==0:
				sys.exit('Can\'t install '+b)
		elif(dist=="windows"):
			os.system('py -3 -m pip install '+b)
		elif(dist=="mac"):
			check_for_root()
			os.system('pip3 install '+b)
	else:
		sys.exit('Please install needed binarys to run this script')

print("Platform: "+sys.platform)
if(sys.platform=="linux"):
	dist = "linux"
elif(sys.platform=="win32"):
	dist = "windows"
elif(sys.platform=="darwin"):
	dist = "mac"
try:
	import numpy as np
except ImportError:
	install_binary("numpy",dist)
	import numpy as np
try:
	import mpmath
except ImportError:
	install_binary("mpmath",dist)
	import mpmath
try:
	import pylab as pl
	import matplotlib.patches as mpatches
except ImportError:
	install_binary("matplotlib",dist)
	import pylab as pl
	import matplotlib.patches as mpatches


class Filtre:
	

	def __init__(self, n=0 , Amax=0, Fc=0, R1=0):
		self.n = n
		self.Fc = Fc
		self.Amax = Amax
		self.Rn = 0.0
		self.r = 0.0
		self.R1 = int(R1)
		self.beta = 0
		self.gamma = 0.0
		self.wc = 0.0  
	
	def construire_Rn(self):
		if(self.n%2 == 1):
			self.r = 1
		elif(self.n%2 == 0):
			self.r = math.tanh(self.beta/4)**2
								
	def calcul_wc(self):
		self.wc = 2*math.pi*self.Fc
	
	def calcul_beta(self):
		self.beta = math.log(mpmath.coth(self.Amax/17.37))

	def calcul_gamma(self):
		self.gamma = math.sinh(self.beta/(2*self.n))

	def calcul_Rn(self):
		self.Rn = self.r*self.R1

	def remplir_tab_a(self):
		for k in range(1,self.n+1):
			a.append(math.sin(((2*k-1)*math.pi)/(2*self.n)))
		return a

	def remplir_tab_b(self):
		gamma_carre = (self.gamma**2)
		for k in range(1,self.n+1):
			b.append( gamma_carre + math.sin((k*math.pi)/self.n)**2)
		return b

	def remplir_tab_g(self, a=[], b=[]):
		g.append(2*a[0]/self.gamma)  #la liste commence à 0 mais k = 1
		for k in range(1,self.n): 
			g.append((4*a[k-1]*a[k])/(b[k-1]*g[k-1]))
		return g

	def remplir_tab_L(self, g=[]):
		r = float(self.R1)/float(self.wc)
		for k in range(0,self.n):
			L.append(r*g[k])
		return L

	def remplir_tab_C(self, g=[]):
		e = (1/self.R1)*(1/self.wc)
		for k in range(0,self.n):
			C.append(e*g[k])
		return C

	def get_wc(self):
		return float(self.wc)



if __name__ == "__main__":

	filtre = Filtre(7,0.5,12*10**8,50)
	a = []
	b = []
	g = []
	L = []
	C = []
	print('Processing needed parameters...',end="")
	
	try:
		filtre.construire_Rn()
		filtre.calcul_Rn()
		filtre.calcul_wc()
		filtre.calcul_beta()
		filtre.calcul_gamma()
		a = filtre.remplir_tab_a()
		b = filtre.remplir_tab_b()
		g = filtre.remplir_tab_g(a,b)
		print_done()
	except:
		print_err()

	print('Calculation of needed capacitor values...',end="")
	try:
		C = filtre.remplir_tab_C(g)
		print_done()
	except:
		print_err()
	print('Calculation of needed coils values...',end="")
	try:
		L = filtre.remplir_tab_L(g)
		print_done()
	except:
		print_err()
	
	"""for k in range(0,filtre.n):
		print("a[%d] = %s " % (k+1,a[k]))
	
	for k in range(0,filtre.n):
		print("b[%d] = %s " % (k+1,b[k]))
	
	#print("len g = %s" % len(g))
	for k in range(0,filtre.n):
		print("g[%d] = %s " % (k+1,g[k]))
	"""
	print("Fc = %F" % filtre.Fc)
	print("beta = %f" % filtre.beta)
	print("n = %f" % filtre.n)
	print("r = %f" % filtre.r)
	print("wc = %f" % filtre.wc)
	print("gamma = %f" % filtre.gamma)

	for k in range(0,filtre.n):
		print("L[%d] = %s \t C[%d] \u27DB = %s " % (k+1,L[k],k+1,C[k]))
	
	#U+27BF   bobine			res:U+2D62		U+27BF		U+16F5
	#print('\u27DB')		U+3022
	y1 = []
	y2 = []
	x = np.linspace(0,filtre.wc,10**4,endpoint=True)
	for i in range(0,10**4):
		w = 2*math.pi*x[i]
		if(w <= 2*math.pi*filtre.Fc):
			y1.append(10*math.log10(1+(10**(filtre.Amax/10) -1)*(math.cos(filtre.n*math.acos(w/filtre.wc))**2)) )
		elif( w >= 2*math.pi*filtre.Fc):
			y2.append(10*math.log10(1+(10**(filtre.Amax/10) -1)*(math.cosh(filtre.n*math.acosh(w/filtre.wc)**2))) )
			i+=1000
	
	y = y1+y2

	#print(x)
	#print(y2)
	pl.ylabel( "A(dB)" ) 
	pl.xlabel( "F(Hz)" ) 
	#print(x)
	pl.axis([0, filtre.Fc*2, -filtre.Amax-2, filtre.Amax+3])
	pl.plot(x,y)
	ligne_Fc= pl.plot([filtre.Fc, filtre.Fc], [-filtre.Amax-2, filtre.Amax], 'r--', lw=0.8, label='Fc')
	ligne_Am= pl.plot([filtre.Fc/2, filtre.Fc/2], [0, filtre.Amax], 'g--', lw=2, label='Am')
	pl.plot([(filtre.Fc/2)-1000, (filtre.Fc/2)+1000], [0, filtre.Amax], 'g--', lw=2,)
	pl.plot(filtre.Fc, y1[len(y1)-1], 'ro')
	red_patch = mpatches.Patch(color='red', label='Fc')
	green_patch = mpatches.Patch(color='green', label='Am')
	pl.legend(handles=[red_patch,green_patch])

	#pl.legend([ligne_Fc, ligne_Am], ['Fc', 'Amax'])
	#pl.plot(x1, F2, 'bx')

	#pl.plot(x2,y2)
	"""pl.plot(L)
	pl.plot(C)"""
	pl.show()