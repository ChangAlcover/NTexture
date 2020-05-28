import numpy as np
import scipy.special as special
import pylab as pl
import quaternion as quat
import time as tm
import scipy.io
import PSpincalc as sp
a=1
b=1
c=1
alfa=90
beta=90
gamma=90

################################################################
#        This file is part of NTexture                         #
#   At the moment you can get the full code at:                #
#   https://github.com/ChangAlcover/NTexture                   #
#                                                              #
#   A publication will be made to explain its functionalities  #
#                                                              #
#   If you use it for your work, we would appreciate it        #
#   if you would use the future reference                      #
#                                                              #
################################################################

#In this file the necessary functions are implemented for the 
#simulation of the cross sections

# Warning: some of these functions are obsolete and will be removed
#          in future or updated versions

# Warning: The functions work correctly for cubics structures only,
#          although the implementation of the rest of the structures 
#          is quite advanced, it is not complete

def tipo_estructura(a,b,c,alfa,beta,gamma):
	if (a==b==c and alfa==beta==gamma==90): return 1    #Cubica
	if (a==b!=c and alfa==beta==gamma==90): return 2	#tetragonal
	if (a!=b!=c and alfa==beta==gamma==90): return 3	#Ortorrombica
	if (a==b==c and alfa==beta and gamma!=90): return 4 #Trigonal
	if (a!=b!=c and alfa!=90 and beta==gamma==90): return 5	#Monoclinica
	if (a!=b!=c and alfa!=beta!=gamma): return 6 		#Triclinica
	if (a==b!=c and alfa==beta==90 and gamma==120): return 7 #Hexagonal
	return 0


def t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l):
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==0): return 0
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==1): return (h**2+k**2+l**2)/a**2
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==2): return h**2/a**2+k**2/a**2+l**2+c**2
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==3): return h**2/a**2+k**2/b**2+l**2/c**2
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==4): return ((h**2+k**2+l**2)*np.sin(np.pi/180*alfa)**2+2*(h*k+k*l+l*h)*(np.cos(np.pi/180*alfa)**2-np.cos(np.pi/180*alfa)))/(a**2*(1+2*np.cos(np.pi/180*alfa)**3-3*np.cos(np.pi/180*alfa)**2))
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==5): return (h**2/a**2+k**2*np.sin(np.pi/180*beta)**2/b**2+b**2/c**2-2*h*l*np.cos(np.pi/180*beta)/(a*c))/np.sin(np.pi/180*beta)**2
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==6): return 0 #Triclinica
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==7): return 4/3*(h**2+k**2+h*k)/a**2+l**2/c**2

def v_0(a,b,c,alfa,beta,gamma): # Eventualmente lo tengo que hacer para todos tipos de estructura
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==1): return a**3



#Read the file with the information of the material
#One line should have the values of sides and angles
#The others lines should have the wickoff position, the scaterring length and mu^2

def read(archivo="Estructura.txt"):
	estr=open(archivo,"r")
	estructura=[]
	for line in estr:
		s=line.split('\t')
		if len (s)==5: 
			estructura.append(s)
		if len (s)==6:
			global a,b,c,alfa,beta,gamma
			a=float(s[0])
			b=float(s[1])
			c=float(s[2])
			alfa=float(s[3])
			beta=float(s[4])
			gamma=float(s[5])
	estr.close()
	return estructura

#From every value of hkl, once the structure is load, the facrot F_s is calculated
def Factor_s(estructura,h,k,l):
	parte_real=0
	parte_imag=0
	for i in range (0,len(estructura)):
		t_x=2*np.pi*(float(estructura[i][0])*h+float(estructura[i][1])*k+float(estructura[i][2])*l)
		parte_real=parte_real+ float(estructura[i][3])*np.exp(-4*np.pi**2*t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)*float(estructura[1][4])/2)*np.exp(-4*np.pi**2*t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)*(float(estructura[i][4])-float(estructura[1][4]))/2)*np.cos(t_x)
		parte_imag=parte_imag+ float(estructura[i][3])*np.exp(-4*np.pi**2*t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)*float(estructura[1][4])/2)*np.exp(-4*np.pi**2*t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)*(float(estructura[i][4])-float(estructura[1][4]))/2)*np.sin(t_x)
	return (parte_real**2+parte_imag**2)*0.01

#Conversion from Bunge angles to quaternion
#not sure if work correctly, just used to quickly calculation

def euler2cuat(rotacion):
	a_1=np.cos(rotacion[1]/2)*np.cos((rotacion[0]+rotacion[2])/2)
	a_2=-np.sin(rotacion[1]/2)*np.sin((rotacion[0]-rotacion[2])/2)
	a_3=np.sin(rotacion[1]/2)*np.cos((rotacion[0]-rotacion[2])/2)
	a_4=np.cos(rotacion[1]/2)*np.sin((rotacion[0]+rotacion[2])/2)
	v=[a_1,a_2,a_3,a_4]
	return quat.quaternion(*v)

# Next two function are the rotacion from Bunge angles and from quaternion
def rot_euler(haz, rotacion):
	haz=np.array([0.] + haz)
	haz = quat.quaternion(*haz)
	q=euler2cuat(rotacion)
	v_prime = q * haz * np.conjugate(q)
	return v_prime.imag

def rot_quat(beam, rot):
	beam=np.array([0.] + beam)
	beam = quat.quaternion(*beam)
	rot = quat.quaternion(*rot)
	v_prime = rot * beam * np.conjugate(rot)
	return v_prime.imag

#lambda_hkl=2*d_hkl*cos(angle between beam and normal)->ang_vextor_normal
def lam_hkl(vector,h,k,l,t_hkl_2):
	aux= 2*np.sqrt(1/t_hkl_2)*np.sin(ang_B(vector,h,k,l))
	return aux

#From the material a list of posible hkl is created, with the value of F_s
#F_s<0.5 are discarted
#The list is sorted by F_s value
def Crear_archivo(estructura):
	salida=open("Lista_hkl.txt",'w')
	lista=[]
	for h in range (-10,10):
		for k in range (-10,10):
			for l in range (-10,10):
				if(h==k==l==0): continue
				aux=Factor_s(estructura,h,k,l)				
				if (aux>0.5):
					lista.append([aux,h,k,l,t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)])
	lista.sort(reverse=True)
	for ii in lista:
		#Print order: h k l F_s t_hkl # With tabular separation
		aux=str(ii[1])+"\t"+str(ii[2])+"\t"+str(ii[3])+"\t"+str(ii[0])+"\t"+str(ii[4])+"\n"
		salida.write(aux)
	salida.close()

#Enginex
def t_Enginex(x):
	return (special.erf((x-1.3934)/0.18492)*(18.94806-10.82914*x)+16.6964*x)/10000
#IMAT
def tau_i(x):
	tau_=(418/(1+155.1*np.exp(-4.46*x)))/(14342)
	return (tau_)

def ang_vector_normal(vector,h,k,l):
	return np.arccos(np.sqrt((vector[0]*h+vector[1]*k+vector[2]*l)**2)/(np.sqrt(h**2+k**2+l**2)*np.sqrt(vector[0]**2+vector[1]**2+vector[2]**2))-0.0000002)

def ang_B(vector,h,k,l):
	return np.arcsin(np.sqrt((vector[0]*h+vector[1]*k+vector[2]*l)**2)/(np.sqrt(h**2+k**2+l**2)*np.sqrt(vector[0]**2+vector[1]**2+vector[2]**2))-0.0000002)

#Gaussian contribution to the width of the peaks
#e-> average elastic deformation of the crystal lattice,
#n->disorientation of the mosaic glass blocks (mosaicity) 
#l->divergencia del haz incidente
def v_hkl(lam_hkl,ang,e,n,l):
	return lam_hkl*np.sqrt(e**2+(l**2+n**2)*(np.tan(ang))**2)


# Important: MAIN FUNCTION
def P (lam,lam_hkl,v_hkl,tau):
	if np.sqrt(v_hkl)<0.05*tau:
		return 1/(2*tau)*np.exp(-(lam-lam_hkl)/tau+v_hkl**2/(2*tau**2))*special.erfc((lam-lam_hkl)/(np.sqrt(2)*v_hkl)-v_hkl/(np.sqrt(2)*tau))
	else:
		return 1/(np.sqrt(2*np.pi)*v_hkl)*np.exp(-(lam-lam_hkl)**2/(2*v_hkl**2))
	

def Leer_archivo(haz,archivo="Lista_hkl.txt",lam_lim=1.5):
	entrada=open(archivo,"r")
	estructura=[]
	for ii in entrada:
		s=ii.split('\t')
		aux_2=lam_hkl(haz,float(s[0]),float(s[1]),float(s[2]),float(s[4]))
		if aux_2>lam_lim: estructura.append([float(s[0]),float(s[1]),float(s[2]),aux_2,float(s[3])])
	entrada.close()		
	return estructura

# For optimization, the values of the main function is calculated only for values near lambda_hkl
def Funcion_pico(h,k,l,haz,lam,inst):
	la_hkl=lam_hkl(haz,h,k,l,t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l))
	if inst==1:
		tau=t_Enginex(la_hkl)
	if inst==2:
		tau=tau_i(la_hkl)
	if inst==3:
		tau=t_Enginex(la_hkl) # This need to be implemented
	vi_hkl=v_hkl(lam_hkl(haz,h,k,l,t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)),ang_vector_normal(haz,h,k,l),0.0001,(0.4)*np.pi/180,8*np.pi/180)#(9.5/60)*np.pi/180)
	estructura=[]
	for i in lam:
		if i<la_hkl-0.8:
			estructura.append(0)
		elif i>la_hkl+0.8:
			estructura.append(0)
		else:
			estructura.append(P(i,la_hkl,vi_hkl,tau))
	return estructura


def mu_hkl (F_s,lam_hkl,ang,v_0):
	return 10**8*F_s*10**(-24)*(lam_hkl*10**(-8))**4/(2*(v_0*10**(-24))**2*(np.sin(ang))**2)

#Simulate one dirrection given by Bunge angles
def Simular_dir(rotacion,haz,lam,lam_lim=1.5):
	new_haz=rot_euler(haz,rotacion)
	estructura=Leer_archivo(new_haz,"Lista_hkl.txt",lam_lim)
	p=np.zeros(1000)
	for i in range(0, len(estructura)):#print(estructura[i][0],estructura[i][1],estructura[i][2],mu_hkl(estructura[i][4],estructura[i][3],ang_vector_normal(rot_euler(new_haz,rotacion),estructura[i][0],estructura[i][1],estructura[i][2]),v_0(a,b,c,alfa,beta,gamma)),lam_hkl(rot_euler(new_haz,rotacion),estructura[i][0],estructura[i][1],estructura[i][2],t_hkl_2(a,b,c,alfa,beta,gamma,estructura[i][0],estructura[i][1],estructura[i][2])))
		p=p+mu_hkl(estructura[i][4],estructura[i][3],ang_B(new_haz,estructura[i][0],estructura[i][1],estructura[i][2]),v_0(a,b,c,alfa,beta,gamma))*np.array(Funcion_pico(estructura[i][0],estructura[i][1],estructura[i][2],new_haz,lam))

		'''
		pl.figure(figsize=(8, 6), dpi=80)
		pl.plot(lam,p,color="red",label="Espectro")
		pl.xlabel("Campo [G]")
		pl.ylabel("Intensidad")
		pl.legend(loc='upper left')
		pl.show()
		'''
	return p

# call the main function for every lambda
def Simular_dir_quat(rot,haz,lam,lam_lim=1.5):
	new_haz=rot_quat(haz,rot)
	estructura=Leer_archivo(new_haz,"Lista_hkl.txt",lam_lim)
	p=np.zeros(len(lam))
	for i in range (0,len(estructura)):
		p=p+mu_hkl(estructura[i][4],estructura[i][3],ang_B(new_haz,estructura[i][0],estructura[i][1],estructura[i][2]),v_0(a,b,c,alfa,beta,gamma))*np.array(Funcion_pico(estructura[i][0],estructura[i][1],estructura[i][2],new_haz,lam))
	return p

# This is old, buy i keep it, maybe will be useful
def Simular_3_dir():
	
	haz=np.array([0.7524,0.0183,0.6304])
	Crear_archivo()
	p=np.zeros(1000)
	lam=np.linspace(2,3.7,1000)  ## Agregue lam como parametro para Simular dir
	pl.figure(figsize=(8, 6), dpi=80)
	p=Simular_dir([0,0,0],haz,lam,2)
	pl.plot(lam,p,color="red",label="0 grados")
	p=Simular_dir([0,0,-0.5*np.pi/180],haz,lam,2)
	pl.plot(lam,p,color="blue",label="1 grado")
	p=Simular_dir([0,0,-1*np.pi/180],haz,lam,2)
	pl.plot(lam,p,color="black",label="2 grados")

	pl.xlabel("Lambda (A)")
	pl.ylabel("Intensidad")
	pl.legend(loc='upper left')
	pl.show()
	

#Create a list of modes for a powder material
def Crear_uniforme(resolucion=4):
	salida=open("modos.txt",'w')
	for i in range (resolucion,90,resolucion):
		for j in range (resolucion,90,resolucion):
			for k in range (resolucion,90,resolucion):
				aux=str(i)+"\t"+str(j)+"\t"+str(k)+"\t1\n"
				salida.write(aux)
	salida.close()


def Leer_modos(archivo="modos.txt"):
	entrada=open(archivo,"r")
	estructura=[]
	for ii in entrada:
		aux=ii.split('\t')
		estructura.append([float(aux[0]),float(aux[1]),float(aux[2]),float(aux[3])])
	entrada.close
	return estructura

def Funcion_modos(haz):
	modos=Leer_modos()
	#Crear_archivo()
	p=np.zeros(1000)
	lam=np.linspace(1.5,5.0,1000)
	print(len (modos))
	for i,ii in enumerate(modos):
		print(i)
		p+=1/len(modos)*Simular_dir([-ii[0]*np.pi/180,-ii[1]*np.pi/180,-ii[2]*np.pi/180],haz,lam)
	pl.figure(figsize=(8, 6), dpi=80)
	pl.plot(lam,p,color="red",label="Espectro")
	pl.xlabel("Lambda(A)")
	pl.ylabel("Intensidad")
	pl.legend(loc='upper left')
	pl.show()
	salida=open("datos.txt",'w')
	for i,j in enumerate (p):
		salida.write(str(j)+"\t"+str(lam[i])+"\n")

#Old way to load .mat files
def Read_ODF(archivo="odf"):
	mat=scipy.io.loadmat(archivo)
	#print(mat.keys())
	datos=mat['odf_espectro']
	salida=open("modos.txt",'w')	
	lista=[]
	for ii in range (0, len(datos[0][0][0][0][0][2])):
		q0=datos[0][0][0][0][0][1][0][0][7][0][0][2][0][0][0][0][0][0][ii][0]
		q1=datos[0][0][0][0][0][1][0][0][7][0][0][2][0][0][0][0][0][1][ii][0]
		q2=datos[0][0][0][0][0][1][0][0][7][0][0][2][0][0][0][0][0][2][ii][0]
		q3=datos[0][0][0][0][0][1][0][0][7][0][0][2][0][0][0][0][0][3][ii][0]
		peso=datos[0][0][0][0][0][2][ii][0]
		lista.append([peso,q0,q1,q2,q3])
	lista.sort(reverse=True)
	for ii in lista:
		aux=str(ii[1])+"\t"+str(ii[2])+"\t"+str(ii[3])+"\t"+str(ii[4])+"\t"+str(ii[0])+"\n"
		salida.write(aux)
	salida.close


def Read_mode_cuat(archivo="modos.txt"):
	entrada=open(archivo,"r")
	estructura=[]
	for ii in entrada:
		aux=ii.split('\t')
		estructura.append([float(aux[0]),float(aux[1]),float(aux[2]),float(aux[3]),float(aux[4])])
	entrada.close
	return estructura

#Next two function are old, but they work fine like a example
def Flor_quat(beam,rot):
	modos=Read_mode_cuat()
	p=np.zeros(1000)
	lam=np.linspace(1.5,5.0,1000)
	print(len (modos))
	for i,ii in enumerate (modos):
		aux=quat.quaternion(*np.array([ii[0],ii[1],ii[2],ii[3]]))
		posicion_rot=rot*aux*np.conjugate(rot)
		#aux=np.array([ii[0],ii[1],ii[2],ii[3]])
		#print(sp.Q2EA(aux,EulerOrder="zxz")*180/np.pi)
		print(i)
		p+=ii[4]*Simular_dir_quat([posicion_rot.w,posicion_rot.x,posicion_rot.y,posicion_rot.z],beam,lam)
	pl.figure(figsize=(8, 6), dpi=80)
	pl.plot(lam,p,color="red",label="Espectro")
	pl.xlabel("Lambda(A)")
	pl.ylabel("Intensidad")
	pl.legend(loc='upper left')
	pl.show()
	salida=open("datos.txt",'w')
	for i,j in enumerate (p):
		salida.write(str(j)+"\t"+str(lam[i])+"\n")

def Flor_quat_2(beam,alpha,beta):
	modos=Read_mode_cuat()
	p=np.zeros(1000)
	lam=np.linspace(1.5,5.0,1000)
	print(len (modos))
	for i,ii in enumerate (modos):
		aux=quat.quaternion(*np.array([ii[0],ii[1],ii[2],ii[3]]))
		rot=euler2cuat([(alpha+95)*np.pi/180,0,0])
		aux=rot*aux*np.conjugate(rot)
		rot=euler2cuat([0,(beta-5)*np.pi/180,0])
		posicion_rot=rot*aux*np.conjugate(rot)
		#aux=np.array([ii[0],ii[1],ii[2],ii[3]])
		#print(sp.Q2EA(aux,EulerOrder="zxz")*180/np.pi)
		print(i)
		p+=ii[4]*Simular_dir_quat([posicion_rot.w,posicion_rot.x,posicion_rot.y,posicion_rot.z],beam,lam)
	pl.figure(figsize=(8, 6), dpi=80)
	pl.plot(lam,p,color="red",label="Espectro")
	pl.xlabel("Lambda(A)")
	pl.ylabel("Intensidad")
	pl.legend(loc='upper left')
	pl.show()
	salida=open("datos.txt",'w')
	for i,j in enumerate (p):
		salida.write(str(j)+"\t"+str(lam[i])+"\n")


#The function used in the main code
def Simular_dir_angles(haz,lam,inst,lam_lim=1.5):
	estructura=Leer_archivo(haz,"Lista_hkl.txt",lam_lim)
	p=np.zeros(len(lam))
	for i in range (0,len(estructura)):
		p=p+mu_hkl(estructura[i][4],estructura[i][3],ang_B(haz,estructura[i][0],estructura[i][1],estructura[i][2]),v_0(a,b,c,alfa,beta,gamma))*np.array(Funcion_pico(estructura[i][0],estructura[i][1],estructura[i][2],haz,lam,inst))
	return p







