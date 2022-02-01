import numpy as np
import scipy.special as special
import scipy.io
from scipy.spatial.transform import Rotation as R
import math as m

def rho_m_n(a,b,c,v):
	if a==0:
	    a=c/v*b/0.6022
	if b==0:
	    b=a*v*0.6022/c
	if c==0:
	    c=round(a*v*0.6022/b)
	return a,b,c

def tipo_estructura(a,b,c,alfa,beta,gamma):
	if (a==b==c and alfa==beta==gamma==90): return 1    #Cubica
	if (a==b!=c and alfa==beta==gamma==90): return 2	#tetragonal
	if (a!=b!=c and alfa==beta==gamma==90): return 3	#Ortorrombica
	if (a==b==c and alfa==beta and gamma!=90): return 4 #Trigonal
	if (a!=b!=c and alfa!=90 and beta==gamma==90): return 5	#Monoclinica
	if (a!=b!=c and alfa!=beta!=gamma): return 6 		#Triclinica
	if (a==b!=c and alfa==beta==90 and gamma==120): return 7 #Hexagonal
	return 0

def v_0(a,b,c,alfa,beta,gamma): # Eventualmente lo tengo que hacer para todos tipos de estructura
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==1): return a**3
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==7): return a**2*c*np.sqrt(3)/2

def inter_extra_polacion(x,y,x_aca):
	y_new=np.zeros(x_aca.shape[0])
	for i,ii in enumerate(x_aca):
		if ii<x[0]:
			m=(y[1]-x[0])/(x[1]-x[0])
			n=-m*x[0]+y[0]
			y_new[i-1]=m*ii+n
		elif ii>x[-1]:
			m=(y[-1]-y[-2])/(x[-1]-x[-2])
			n=-m*x[-1]+y[-1]
			y_new[i-1]=m*ii+n
		else:
			for j,jj in enumerate(x):
				if ii>jj:
					m=(y[j+1]-y[j])/(x[j+1]-x[j])
					n=-m*jj+y[j]
					y_new[i]=m*ii+n
	return y_new

def inter_points(x,y,x1):
	if x1<1 or x1>10:
		return 0
	for i,ii in enumerate(x):
		if float(ii)>x1:
			return (float(y[i])-float(y[i-1]))*(x1-float(x[i-1]))/(float(ii)-float(x[i-1]))+float(y[i-1])

def feel_lucky(archivo="/home/chang/Desktop/NTexture/ODF_data_base/ODF_Cu.mat"):
	mat=scipy.io.loadmat(archivo)
	###Cambiar la siguiente linea, urgente
	datos=mat['odf1']
	#print(len(datos[0][0][0][0][0][1][0][0][7][0][0][2][0][0][0][0][0][2]))
	lista=[]
	'''
	for ii in range (0, len(datos[0][0][0][2])):
		q0=datos[0][0][0][1][0][0][7][0][0][2][0][0][0][0][0][0][ii][0]
		q1=datos[0][0][0][1][0][0][7][0][0][2][0][0][0][0][0][1][ii][0]
		q2=datos[0][0][0][1][0][0][7][0][0][2][0][0][0][0][0][2][ii][0]
		q3=datos[0][0][0][1][0][0][7][0][0][2][0][0][0][0][0][3][ii][0]
		r = R.from_quat([[q0,q1,q2,q3]])
		peso=datos[0][0][0][2][ii][0]
		#print(r.as_euler('zxz',degrees=True)[0])
		lista.append([peso,r.as_euler('zxz',degrees=True)[0][0],r.as_euler('zxz',degrees=True)[0][1],r.as_euler('zxz',degrees=True)[0][2]])
	'''
	
	try:
		for ii in range (0, len(datos[0][0][2])):
			if len(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][0])==1:
				q0=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][0][0][ii])
				q1=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][1][0][ii])
				q2=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][2][0][ii])
				q3=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][3][0][ii])
				w=float(datos[0][0][2][ii][0])
			else:
				q0=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][0][ii][0])
				q1=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][1][ii][0])
				q2=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][2][ii][0])
				q3=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][3][ii][0])
				w=float(datos[0][0][2][ii][0])
			r = R.from_quat([[q0,q1,q2,q3]])
			lista.append([w,r.as_euler('zxz')[0][0],r.as_euler('zxz')[0][1],r.as_euler('zxz')[0][2]])
			lista.sort()

	except:
		messagebox.showinfo('Error: Invalid data','Sorry, we can\'t read the format data, please search over allowed formats')

	lista.sort(reverse=True)
	return lista

def neutron_path_points(arr1,arr2,arr3,inf1,sup1,inf2,sup2,rec):
	aux=[]
	for i, ii in enumerate(arr1):
		if ii>inf1 and ii<sup1:
			if arr2[i]>inf2 and arr2[i]<sup2:
				aux.append(arr3[i])
	if len(aux)==0 or len (aux)==1:
		if rec==1:
			return [0,0]
		aux2 = neutron_path_points(arr1,arr2,arr3,inf1-(sup1-inf1),sup1+(sup1-inf1),inf2-(sup2-inf2),sup2+(sup2-inf2),1)
		if aux2[0]==0 and aux2[1]==0:
			return [0,0]
		else:
			return aux2

	maximo=max(aux)
	minimo=min(aux)
	aux_min=[]
	aux_max=[]
	for ii in aux:
		if ii <(maximo+minimo)/2:
			aux_min.append(ii)
		else:
			aux_max.append(ii)
	if len(aux_min)==0 or len (aux_max)==0:
		return [0,0]
	return [sum(aux_min)/len(aux_min),sum(aux_max)/len(aux_max)]

def minimos_maximos(arr,beam):
	x=np.reshape(arr[0],(1,-1))
	y=np.reshape(arr[1],(1,-1))
	z=np.reshape(arr[2],(1,-1))
	if beam=="Z axis":
		return([np.round(min(x[0]),decimals=1),np.round(max(x[0]),decimals=1),np.round(min(y[0]),decimals=1),np.round(max(y[0]),decimals=1)])
	if beam=="Y axis":
		return([np.round(min(x[0]),decimals=1),np.round(max(x[0]),decimals=1),np.round(min(z[0]),decimals=1),np.round(max(z[0]),decimals=1)])
	if beam=="X axis":
		return([np.round(min(y[0]),decimals=1),np.round(max(y[0]),decimals=1),np.round(min(z[0]),decimals=1),np.round(max(z[0]),decimals=1)])

### 
def Factor_s(estructura,h,k,l,a,b,c,alfa,beta,gamma):
	parte_real=0
	parte_imag=0
	for i in range (0,len(estructura)):
		t_x=2*np.pi*(float(estructura[i][0])*h+float(estructura[i][1])*k+float(estructura[i][2])*l)
		parte_real=parte_real+ float(estructura[i][3])*np.exp(-4*np.pi**2*t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)*float(estructura[1][4])/2)*np.exp(-4*np.pi**2*t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)*(float(estructura[i][4])-float(estructura[1][4]))/2)*np.cos(t_x)
		parte_imag=parte_imag+ float(estructura[i][3])*np.exp(-4*np.pi**2*t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)*float(estructura[1][4])/2)*np.exp(-4*np.pi**2*t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)*(float(estructura[i][4])-float(estructura[1][4]))/2)*np.sin(t_x)
	return (parte_real**2+parte_imag**2)*0.01

def Factor_s_hex(a,c,h,k,l,sigmacoh,u02):
	V=a**2*c*np.sqrt(3)/2
	q=R.from_rotvec(np.pi/3*np.array([0,0,1]))
	b1=np.pi*2/V*c*a*np.array([1/2,np.sqrt(3)/2,0])
	b2=q.apply(b1)
	b3=2*np.pi/c*np.array([0,0,1])
	G=h*b1+k*b2+l*b3
	norm_G=np.linalg.norm(G)
	f_i=sigmacoh/(2*np.pi)*np.exp(-norm_G**2*u02)
	F_hkl=4*f_i*np.cos(np.pi*(h/3+2*k/3+l/2))**2
	return F_hkl

def t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l):
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==0): return 0
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==1): return (h**2+k**2+l**2)/a**2
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==2): return h**2/a**2+k**2/a**2+l**2+c**2
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==3): return h**2/a**2+k**2/b**2+l**2/c**2
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==4): return ((h**2+k**2+l**2)*np.sin(np.pi/180*alfa)**2+2*(h*k+k*l+l*h)*(np.cos(np.pi/180*alfa)**2-np.cos(np.pi/180*alfa)))/(a**2*(1+2*np.cos(np.pi/180*alfa)**3-3*np.cos(np.pi/180*alfa)**2))
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==5): return (h**2/a**2+k**2*np.sin(np.pi/180*beta)**2/b**2+b**2/c**2-2*h*l*np.cos(np.pi/180*beta)/(a*c))/np.sin(np.pi/180*beta)**2
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==6): return 0 #Triclinica
	if (tipo_estructura(a,b,c,alfa,beta,gamma)==7): return 4/3*(h**2+k**2+h*k)/a**2+l**2/c**2

def lam_hkl(vector,h,k,l,t_hkl_2):
	aux= 2*np.sqrt(1/t_hkl_2)*np.sin(ang_B(vector,h,k,l))
	#print(aux,h,k,l,vector)
	return aux

def ang_B(vector,h,k,l):
	return np.arcsin(np.sqrt((vector[0]*h+vector[1]*k+vector[2]*l)**2)/(np.sqrt(h**2+k**2+l**2)*np.sqrt(vector[0]**2+vector[1]**2+vector[2]**2))-0.0000002)
def ang_vector_normal(vector,h,k,l):
	return np.arccos(np.sqrt((vector[0]*h+vector[1]*k+vector[2]*l)**2)/(np.sqrt(h**2+k**2+l**2)*np.sqrt(vector[0]**2+vector[1]**2+vector[2]**2))-0.0000002)
def mu_hkl (F_s,lam_hkl,ang,v_0):
	return 10**8*F_s*10**(-24)*(lam_hkl*10**(-8))**4/(2*(v_0*10**(-24))**2*(np.sin(ang))**2)

def v_hkl(lam_hkl,ang,e,n,l):
	return lam_hkl*np.sqrt(e**2+(l**2+n**2)*(np.tan(ang))**2)

#Enginex
def t_Enginex(x):
	return (special.erf((x-1.3934)/0.18492)*(18.94806-10.82914*x)+16.6964*x)/10000
#IMAT
def tau_i(x):
	tau_=(418/(1+155.1*np.exp(-4.46*x)))/(14342)
	return (tau_)

def Crear_Lista_hkl(estructura,a,b,c,alfa,beta,gamma):
	lista=[]
	for h in range (-10,10):
		for k in range (-10,10):
			for l in range (-10,10):
				if(h==k==l==0): continue
				if (tipo_estructura(a,b,c,alfa,beta,gamma)==1): 
					aux=Factor_s(estructura,h,k,l,a,b,c,alfa,beta,gamma)	
				elif (tipo_estructura(a,b,c,alfa,beta,gamma)==7): 
					aux=Factor_s_hex(a,c,h,k,l,float(estructura[0][3]),float(estructura[0][4]))
				else:
					aux=0
				aux2=t_hkl_2(a,b,c,alfa,beta,gamma,h,k,l)						
				if aux>0.5:
					lista.append([aux,h,k,l,aux2])
	lista.sort(reverse=True)
	return lista

def P_0 (lam,lam_hkl,v_hkl,tau):
	if np.sqrt(v_hkl)<0.05*tau:
		return 1/(2*tau)*np.exp(-(lam-lam_hkl)/tau+v_hkl**2/(2*tau**2))*special.erfc((lam-lam_hkl)/(np.sqrt(2)*v_hkl)-v_hkl/(np.sqrt(2)*tau))
	else:
		return 1/(np.sqrt(2*np.pi)*v_hkl)*np.exp(-(lam-lam_hkl)**2/(2*v_hkl**2))

def P (lam,lam_hkl,v_hkl,tau):
	#if v_hkl<0.05*tau:
	#	return 1/(2*tau)*np.exp(-(lam-lam_hkl)/tau+v_hkl**2/(2*tau**2))*(1+special.erf((lam-lam_hkl)/(np.sqrt(2)*v_hkl)-v_hkl/(np.sqrt(2)*tau)))
	#else:
	return np.sqrt(2/np.pi)/v_hkl/(special.erf(lam_hkl/(np.sqrt(2)*v_hkl))+1)*np.exp(-(lam-lam_hkl)**2/(2*v_hkl**2))

def Funcion_pico(h,k,l,vector,lam,la_hkl,inst,e,l1,n):

	#if lam<la_hkl-3 or lam>la_hkl+3:
	#	if P(lam,la_hkl,v_hkl(la_hkl,ang_vector_normal(vector,h,k,l),e,l1,n),t_Enginex(la_hkl))>0.1:
	#		print("Me equivoque haciendo 0 esto en:",P(lam,la_hkl,v_hkl(la_hkl,ang_vector_normal(vector,h,k,l),e,l1,n),t_Enginex(la_hkl)))
	#	valor=0
	#else:
	if inst==1:
		tau=t_Enginex(la_hkl)
	if inst==2:
		tau=tau_i(la_hkl)
	if inst==3:
		tau=t_Enginex(la_hkl) # This need to be implemented
	vi_hkl=v_hkl(la_hkl,ang_vector_normal(vector,h,k,l),e,l1,n)
	valor=P(lam,la_hkl,vi_hkl,tau)
	return valor

def Simular_lam(lam,lista,vector,v_0,inst,e,l,n):
	aux=np.zeros(len(lam))
	for i in range (0,len(lista)):
		if lam_hkl(vector,lista[i][1],lista[i][2],lista[i][3],lista[i][4])> 1:
			aux+=mu_hkl(lista[i][0],lam_hkl(vector,lista[i][1],lista[i][2],lista[i][3],lista[i][4]),ang_B(vector,lista[i][1],lista[i][2],lista[i][3]),v_0)*Funcion_pico(lista[i][1],lista[i][2],lista[i][3],vector,lam,lam_hkl(vector,lista[i][1],lista[i][2],lista[i][3],lista[i][4]), inst,e,l,n)
	return aux

def simular_miguel(coef_four,estructura,vector,V,b1,b2,b3,lam):

	N=1
	L_max=20

	i_l=ind_l(L_max)
	
	sigma_total=np.zeros(lam.shape[0])

	for indice,lam_e in enumerate(lam):
		k_i=np.pi*2/lam_e
		k_v=k_i*vector  #np.array([1,0,0])
		valor=0
		for i,ii in enumerate(estructura):
			G=ii[1]*b1+ii[2]*b2+ii[3]*b3
			norm_G=np.linalg.norm(G)
			if norm_G!=0 and (1-norm_G/2/k_i)>0 and norm_G<10*np.linalg.norm(b3):
				F_hkl=ii[0]
				#f_i=sigmacoh/(2*np.pi)*np.exp(-norm_G**2*u02)
				#F_hkl=4*f_i*np.cos(np.pi*(h/3+2*k/3+l/2))**2
				[rho_k,theta_k]=cart2sph(k_v)
				[rho_G,theta_G]=cart2sph(G)
				#pre_factor=np.zeros(L_max)
				#coef_tex=np.zeros(L_max)
				text_coef=0
				for l_t in range (0,L_max-1):
					pre_factor=4*np.pi/(2*l_t+1)*special.lpmv(0,l_t,norm_G/2/k_i)
					m_ones=( (1**(np.arange(1,(2*(l_t+1))))).reshape((2*l_t+1),1))@((1**(np.arange(1,(2*(l_t+1))))).reshape(1,(2*l_t+1)))
					m_y=special.sph_harm(np.arange(-l_t,l_t+1),l_t,rho_G,theta_G).reshape(2*l_t+1,1)@np.conjugate(special.sph_harm(np.arange(-l_t,l_t+1),l_t,rho_k,theta_k).reshape(1,2*l_t+1))
					m_Clmn=coef_four[int(i_l[l_t]):int(i_l[l_t+1])].reshape(l_t*2+1,l_t*2+1)							
					coef_tex=np.multiply(m_y,m_Clmn).sum()
					text_coef+=pre_factor*coef_tex
				#text_coef=np.dot(coef_tex.reshape(1,-1),pre_factor.reshape(-1,1))
				valor+=N*(2*np.pi)**3/(V*k_i**3)*F_hkl*k_i/(2*norm_G)*text_coef
		sigma_total[indice]=valor
		#print(lam_e,type(valor))
	return sigma_total

def ind_l(Lmax=40):
	l=np.zeros(Lmax)
	l[0]=0
	for i in range(0,Lmax-1):
		l[i+1]=l[i]+(2*i+1)**2
	return l

def cart2sph(vector):
	aux=vector[0]**2+vector[1]**2
	rho=m.atan2(m.sqrt(aux),vector[2]) #xy-z
	theta=m.atan2(vector[1],vector[0])
	return rho, theta