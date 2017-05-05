#!/usr/bin/python3
#-*- coding: utf-8 -*-

#titre           :tchebysheff.py
#description     :Ce code permet le calcul des éléments localisés d'un filtre passe bas de tchebytcheff
#autheurs        :EL IDRISSI, FARGEAS, LAHBABI, PION, VARILLON
#date            :2017/03/29
#version         :0.4
#usage           :
#				 - Linux & MAC: "python3 tchebysheff.py" ou sinon en root "sudo python3 tchebytsheff.py"
#				 - Windows : Un clique sur le fichier, sinon en console avec "py -3 tchebysheff.py"
#					En ligne de commande dans les trois cas il faut être dans le même répértoire que le fichier!!!! 
#python_version  :3 indispensable pour le bon fonctionnement du programme
#==============================================================================

import os
import sys
import math



def print_done():
    print("[Fait]")
    
def print_ok():
    print("[OK]")
    
def print_err():
    print("[Erreur]")

def check_for_root():
	print('\nVérification des droits administrateurs...',end="")
	if not os.geteuid() == 0:
		print_done()
		sys.exit('\nLe programme a besoin des droits administrateurs afin d\'installer les librairies dont il dépend.')
	print_ok()


def install_binary(b="",dist=""):
	print("La librairie "+b+" n'exist pas.")
	if input("Voulez-vous l'installer? [o/n] ").lower() == 'o':
		if(dist=="linux"):
			check_for_root()
			if not os.system('apt-get install python3-'+b)==0:
				sys.exit('\n\nErreur lors de l\'installation, vérifier que vous disposez d\'une connection internet.')
		elif(dist=="windows"):
			if not os.system('py -3 -m pip install '+b)==0:
				sys.exit('\n\nErreur lors de l\'installation, vérifier que vous disposez d\'une connection internet.')
		elif(dist=="mac"):
			check_for_root()
			if not os.system('pip3 install '+b)==0:
				sys.exit('\n\nErreur lors de l\'installation, vérifier que vous disposez d\'une connection internet. ')
		print("\n\nInstallation de "+b+" terminé.")
	else:
		sys.exit('Veuillez installer les librairies utiles pour lancer ce programme.')

print("\n" * 100)
print("\t\t\t*********************************************");
print("\t\t\t*\t   Filtre de tchebysheff\t    *");
print("\t\t\t*********************************************");
print("\n\nPlatforme: "+sys.platform+"\n")
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
			L.append(float(r*g[k]))
		return L

	def remplir_tab_C(self, g=[]):
		e = (1/self.R1)*(1/self.wc)
		for k in range(0,self.n):
			C.append(float(e*g[k]))
		return C

	def get_wc(self):
		return float(self.wc)


def affichage_courbe(filtre):
	y1 = []
	y2 = []
	x = np.linspace(0,filtre.wc,10**4,endpoint=True)
	for i in range(0,10**4):
		w = 2*math.pi*x[i]
		if(w <= 2*math.pi*filtre.Fc):
			y1.append(-1*10*math.log10(1+(10**(filtre.Amax/10) -1)*(math.cos(filtre.n*math.acos(w/filtre.wc))**2)) )
		elif( w >= 2*math.pi*filtre.Fc):
			y2.append(-1*10*math.log10(1+(10**(filtre.Amax/10) -1)*(math.cosh(filtre.n*math.acosh(w/filtre.wc)**2))) )
			i+=1000
	
	y = y1+y2

	pl.ylabel( "G(dB)" ) 
	pl.xlabel( "F(Hz)" ) 
	#définition des unité des axes x,y
	pl.axis([0, filtre.Fc*2, -filtre.Amax-4, filtre.Amax+1])
	pl.plot(x,y)

	#montrer la fréquence de coupure, ainsi que l'atténuation Am 
	ligne_Fc= pl.plot([filtre.Fc, filtre.Fc], [-filtre.Amax-4, filtre.Amax], 'r--', lw=0.8, label='Fc')
	ligne_Am= pl.plot([filtre.Fc/2, filtre.Fc/2], [0, -filtre.Amax], 'g--', lw=2, label='Am')
	pl.plot(filtre.Fc, y1[len(y1)-1], 'ro')
	
	#legende
	red_patch = mpatches.Patch(color='red', label='Fc')
	green_patch = mpatches.Patch(color='green', label='Am')
	pl.legend(handles=[red_patch,green_patch])
	pl.show()



def saisie_chiffre(nom,type):
	funs = {'int': int, 'float': float}
	x = 0
	mauvaise_saisie = True
	while mauvaise_saisie:
		x = input("\nSaisissez l'%s: " % nom)
		try:
			x = funs[type](x)
			if(x<=0):
				print("\nVeuillez saisir une valeur positive")
			else:
				mauvaise_saisie = False
		except:
			print("\nLa valeur que vous avez saisie n'est pas un entier")
	return x


def saisir_Fc():
	unite = {'G': 10**9, 'M': 10**6, 'K': 10**3}
	mauvaise_saisie = True
	i = 0
	r = []
	u = 1
	l = []
	while mauvaise_saisie:
		Fc = 0
		i = 0
		if(len(l) != 0):
			del l[:]
		try:
			Fc = input("\nSaisissez la fréquence de coupure (ex: 40Ghz): ")
			l = list(Fc)
			
			if (len(l)<3):
				print("\nSaisie invalide")
			else:
				for x in l:
					try:
						l[i] = int(x)
						r.append(l[i])
					except:
						l[i] = x
					i += 1
				if(' ' in l) :  #il y a un espace dans la saisie
					l.remove(' ')
				if isinstance(l[-2], str) & isinstance(l[-1], str): 
					if((l[-2]+l[-1]).lower() != 'hz'):
						print("\nL'unité doit être (hz)")
						continue
				if isinstance(l[-3], str):
					if((l[-3]).upper() not in unite):
						print('\nUnité inconnue %s' % l[-3])
						continue
					else:
						u = unite[l[-3].upper()]
				mauvaise_saisie = False
		except:
			exit("\nErreur non traitée")
	m = len(r)-1
	res = 0
	for i in range(0,len(r)):
		res = r[i]*10**(m) + res
		m -= 1
	res = res*u
	return res
	


def saisie():
	n = saisie_chiffre('ordre du filtre','int')
	Amax = saisie_chiffre('atténuation dans la bande en (dB)','float')
	Fc = saisir_Fc()
	R1 = saisie_chiffre('impédence d\'entrée','int')
	
	return n,Amax,Fc,R1


if __name__ == "__main__":
	print("\t\t")
	try: 
		n,Amax,Fc,R1 = saisie()
		filtre = Filtre(n,Amax,Fc,R1)
		a = []
		b = []
		g = []
		L = []
		C = []
		print('\nCalcul des paramètres nécessaires...',end="")
		
		try:
			filtre.calcul_beta()
			filtre.calcul_gamma()
			filtre.construire_Rn()
			filtre.calcul_Rn()
			filtre.calcul_wc()
			a = filtre.remplir_tab_a()
			b = filtre.remplir_tab_b()
			g = filtre.remplir_tab_g(a,b)
			print_done()
		except:
			print_err()

		print('\nCalcul des valeurs des condensateurs...',end="")
		try:
			C = filtre.remplir_tab_C(g)
			print_done()
		except:
			print_err()
		print('\nCalcul des valeurs des bobines...',end="")
		try:
			L = filtre.remplir_tab_L(g)
			print_done()
		except:
			print_err()
		
		
		print("\nFc = %5g Hz" % int(filtre.Fc))
		print("beta = %f" % filtre.beta)
		print("n = %d" % int(filtre.n))
		print("r = %4g" % filtre.r)
		print("wc = %.5g rad/s" % filtre.wc)
		print("gamma = %5g\n\n" % filtre.gamma)



		print("R1 = %s Ohms\n"% filtre.R1)
		if(filtre.n%2==1):
			i = 1
			while i <= filtre.n :
				if i == filtre.n:
					print("C[%d] = %.5g F\n" % (i,C[i-1]))
				else:
					print("C[%d] = %.5g F\n" % (i,C[i-1]))
					print("L[%d] = %.5g H\n" % (i+1,L[i]))
				i += 2
		elif(filtre.n%2==0):
			i = 1
			while i <= filtre.n :
				print("C[%d] = %.5g F\n" % (i,C[i-1]))
				print("L[%d] = %.5g H\n" % (i+1,L[i]))
				i += 2
		print("Rn = %.4g Ohms\n"% filtre.Rn)

		affichage_courbe(filtre)
	except KeyboardInterrupt:
		exit("\n\n\n")
