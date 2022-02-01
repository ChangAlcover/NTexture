import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R
import pickle
#Python file with the classes used in NTexture

##Class Project, gruop all 
#It is used to know in which step the user is

class Project:
	simulation=[]

	def __init__(self,name="Last_proyect"):
		self.name=name

	def add_simulation(self,sim):
		self.simulation.append(sim)

	def delete_simulation(self,sim):
		self.simulation.pop(sim)

	def save_project(self,name):
		with open(name,'wb') as output:
			pickle.dump(self.simulation,output)
	def load_project(self,name):
		with open(name,'rb') as input:
			aux=pickle.load(input)
			for ii in aux:
				self.add_simulation(ii)
		return self



class Simulation:

	def __init__(self, num):
		self.mat=Material()
		self.geo=Geometry()
		self.rot=0
		self.ODF=ODF(0)
		self.B_I=0
		self.num=num
		self.Ins=0
		self.beam="Z axis" 

	def add_material(self,mat):
		self.mat=mat      ## Quizas agregar una notificacion que se esta cambiando
	def add_rot(self,rot):
		self.rot=rot
	def add_B_I(self,data):
		self.B_I=data
	def add_geometry(self,geo):
		self.geo=geo
	def add_ODF(self,ODF):
		self.ODF=ODF
	def add_I(self,num): #EnginX=1,Imat=2, New=3,Astor=4
		self.Ins=num
	def add_beam(self,beam):## Values can be Z axis- Y axis X axis
		self.beam=beam


##Class Material, with aal the information of the sample material
#Users can choose don't load the cross section
#it should be allowed to modify any parameter in the last step


class Material:

	def __init__(self):
		self.name=""
		self.a=0
		self.b=0
		self.c=0
		self.alfa=0
		self.beta=0
		self.gamma=0
		self.rho=0
		self.M=0
		self.N=0
		self.struct=[]
		self.lam=[]
		self.ab=[]
		self.sec=[]
		self.el=[]
		self.dir=""
	def add_mat(self,a):
		self.name=a.name
		self.a=a.a
		self.b=a.b
		self.c=a.c
		self.alfa=a.alfa
		self.beta=a.beta
		self.gamma=a.gamma
		self.rho=a.rho
		self.M=a.M
		self.N=a.N
		self.struct=a.struct
		self.lam=a.lam 
		self.ab=a.ab #Absorption
		self.sec=a.sec #Elastic, without coherent
		self.el=a.el #Section, Elastic Coherent
	def add_name(self,name):
		self.name=name
	def add_dir(self,dir):
		self.dir=dir
	def add_lattice(self,a,b,c,d,e,f):
		self.a=a
		self.b=b
		self.c=c
		self.alfa=d
		self.beta=e
		self.gamma=f	
	def add_data(self,a,b,c):
		if a=="":
			self.rho=0
			self.M=float(b)
			self.N=float(c)
		elif b=="":
			self.rho=float(a)
			self.M=0
			self.N=float(c)
		elif c=="":
			self.rho=float(a)
			self.M=float(b)
			self.N=0
		else:
			self.rho = float(a)
			self.M = float(b)
			self.N = float(c)

	def add_estruct(self,tree):
		aux=tree.get_children()
		for ii in aux:
			self.struct.append(tree.item(ii)['values'])
	##Users can enter coherent elastic component or omit it
	def add_section(self,arch):
		aux=open(arch,"r")
		aux=aux.readlines()
		for line in aux:
			s=line.split('\t')
			if len(s)==4:
				self.lam.append(float(s[0]))
				self.sec.append(float(s[1]))
				self.ab.append(float(s[2]))
				self.el.append(float(s[3]))
			if len (s)==3:
				self.lam.append(float(s[0]))
				self.sec.append(float(s[1]))
				self.ab.append(float(s[2]))
	def add_sec(self,a):
		self.sec=a
	def add_abs(self,a):
		self.ab=a
	def add_el(self,a):
		self.el=a

	def save_material(self,name):
		with open(name,'wb') as output:
			pickle.dump(self,output)
		'''
		file=open(name,"w")
		file.write(str(self.a)+'\t'+str(self.b)+'\t'+str(self.c)+'\t'+str(self.alfa)+'\t'+str(self.beta)+'\t'+str(self.gamma)+'\n')
		for ii in self.struct:
			file.write(str(ii[0])+'\t'+str(ii[1])+'\t'+str(ii[2])+'\t'+str(ii[3])+'\t'+str(ii[4])+'\n')
		if len (self.lam)==len(self.el):
			for i in range (len(self.lam)):
				file.write(str(self.lam[i])+'\t'+str(self.sec[i])+'\t'+str(self.el[i])+'\n')
		else:
			for i in range (len(self.lam)):
				file.write(str(self.lam[i])+'\t'+str(self.sec[i])+'\n')
		file.close()
		'''
	def load_material(self,name):
		with open(name,'rb') as input:
			self=pickle.load(input)
		return self

		'''
		file=open(name,'r')
		self.struct=[]
		self.lam=[]
		self.sec=[]
		self.el=[]
		data=file.readlines()
		for ii in data:
			aux=ii.strip().split('\t')
			if len (aux)==6:
				self.add_lattice(aux[0],aux[1],aux[2],aux[3],aux[4],aux[5])
			if len (aux)==5:
				self.struct.append(aux)
			if len (aux)==3:
				self.lam.append(aux[0])
				self.sec.append(aux[1])
				self.el.append(aux[2])
			if len(aux)==2:
				self.lam.append(aux[0])
				self.sec.append(aux[1])
		file.close()
		'''

class Geometry:

	def __init__(self,type="1",data=[]):
		self.type=type
		if type == "2": #Cylinder [r,h]
			self.r=data[0]
			self.h=data[1]
		if type == "3": # Sphere (r)
			self.r=data[0]
		if type == "5": #Orthohedron [a,b,c]
			self.a=data[0]
			self.b=data[1]
			self.c=data[2]
		self.mov=[0,0,0]
		self.rot=[]
	def move(self,move):
		self.mov=move
	def add_rotation(self,rot):
		self.rot.append(rot)

	def draw(self,fig):
		if self.type=="2":
			self.draw_cylinder(fig)
		if self.type=="3":
			self.draw_sphere(fig)
		if self.type=="5":
			self.draw_Orthohedron(fig)

	def get_points(self,num=200):
		if self.type== "2": return self.points_cylinder(num)
		if self.type=="3": return self.points_sphere(num)
		if self.type=="5": return self.points_Orthohedron(num)

	def points_cylinder(self,num=200):

		h=float(self.h)
		r=float(self.r)

		u = np.linspace(0, 2 * np.pi, num)
		H=np.linspace(-h/2,h/2,num)
		Ra=np.linspace(0,r,num)
		x_1=r*np.outer(np.cos(u),np.ones(num))
		y_1=r*np.outer(np.sin(u),np.ones(num))
		z_1= np.outer(np.ones(num), H)

		x_2=np.outer(np.cos(u),Ra)
		y_2=np.outer(np.sin(u),Ra)
		z_2=np.outer(np.ones(num),h/2*np.ones(num))


		x_3=np.outer(np.cos(u),Ra)
		y_3=np.outer(np.sin(u),Ra)
		z_3=np.outer(np.ones(num),-h/2*np.ones(num))

		x=np.concatenate((x_1,x_2,x_3),axis=0)+self.mov[0]
		y=np.concatenate((y_1,y_2,y_3),axis=0)+self.mov[1]
		z=np.concatenate((z_1,z_2,z_3),axis=0)+self.mov[2]

		for rot in self.rot:
			r = R.from_euler(rot[0], [rot[1], rot[2] ,rot[3]], degrees=True)
			for i,a in enumerate(x):
				for j,b in enumerate(a):
					aux=np.array([x[i][j],y[i][j],z[i][j]])
					aux=r.apply(aux)
					x[i][j]=aux[0]
					y[i][j]=aux[1]
					z[i][j]=aux[2]
		return [x,y,z]

	def draw_cylinder(self,fig):	
		aux=self.points_cylinder()
		fig.set_xticks([np.amin(aux[0]),(np.amin(aux[0])+np.amax(aux[0]))/2,np.amax(aux[0])])
		fig.set_yticks([np.amin(aux[1]),(np.amin(aux[1])+np.amax(aux[1]))/2,np.amax(aux[1])])
		fig.set_zticks([np.amin(aux[2]),(np.amin(aux[2])+np.amax(aux[2]))/2,np.amax(aux[2])])
		fig.set_xlabel("X")
		fig.set_ylabel("Y")
		fig.set_zlabel("Z")
		fig.plot_surface(aux[0], aux[1], aux[2], color='b')

	def points_sphere(self,num=200):
		Ra=float(self.r)
		u=np.linspace(0,2*np.pi,num)
		v=np.linspace(0,np.pi,num)
		x=Ra*np.outer(np.cos(u),np.sin(v))+self.mov[0]
		y=Ra*np.outer(np.sin(u),np.sin(v))+self.mov[1]
		z=Ra*np.outer(np.ones(num),np.cos(v))+self.mov[2]

		for rot in self.rot:
			r = R.from_euler(rot[0], [rot[1], rot[2] ,rot[3]], degrees=True)
			for i,a in enumerate(x):
				for j,b in enumerate(a):
					aux=np.array([x[i][j],y[i][j],z[i][j]])
					aux=r.apply(aux)
					x[i][j]=aux[0]
					y[i][j]=aux[1]
					z[i][j]=aux[2]
		return [x,y,z]

	def draw_sphere(self,fig):
		aux=self.points_sphere()

		
		fig.set_xticks([np.amin(aux[0]),(np.amin(aux[0])+np.amax(aux[0]))/2,np.amax(aux[0])])
		fig.set_yticks([np.amin(aux[1]),(np.amin(aux[1])+np.amax(aux[1]))/2,np.amax(aux[1])])
		fig.set_zticks([np.amin(aux[2]),(np.amin(aux[2])+np.amax(aux[2]))/2,np.amax(aux[2])])
		fig.set_xlabel("X")
		fig.set_ylabel("Y")
		fig.set_zlabel("Z")
		fig.plot_surface(aux[0], aux[1], aux[2], color='b')

	def points_Orthohedron(self,num=200):
		a=float(self.a)
		b=float(self.b)
		c=float(self.c)

		A=np.linspace(-a/2,a/2,num)
		B=np.linspace(-b/2,b/2,num)
		C=np.linspace(-c/2,c/2,num)

		x_1=np.outer(np.ones(num),-a/2*np.ones(num))
		y_1=np.outer(B,np.ones(num))
		z_1=np.outer(np.ones(num),C)

		x_2=np.outer(np.ones(num),a/2*np.ones(num))
		y_2=np.outer(B,np.ones(num))
		z_2=np.outer(np.ones(num),C)

		x_3=np.outer(np.ones(num),A)
		y_3=np.outer(np.ones(num),-b/2*np.ones(num))
		z_3=np.outer(C,np.ones(num))

		x_4=np.outer(np.ones(num),A)
		y_4=np.outer(np.ones(num),b/2*np.ones(num))
		z_4=np.outer(C,np.ones(num))

		x_5=np.outer(A,np.ones(num))
		y_5=np.outer(np.ones(num),B)
		z_5=np.outer(np.ones(num),-c/2*np.ones(num))

		x_6=np.outer(A,np.ones(num))
		y_6=np.outer(np.ones(num),B)
		z_6=np.outer(np.ones(num),c/2*np.ones(num))

		x=np.concatenate((x_1,x_2,x_3,x_4,x_5,x_6),axis=0)+self.mov[0]
		y=np.concatenate((y_1,y_2,y_3,y_4,y_5,y_6),axis=0)+self.mov[1]
		z=np.concatenate((z_1,z_2,z_3,z_4,z_5,z_6),axis=0)+self.mov[2]

		for rot in self.rot:
			r = R.from_euler(rot[0], [rot[1], rot[2] ,rot[3]], degrees=True)
			for i,a in enumerate(x):
				for j,b in enumerate(a):
					aux=np.array([x[i][j],y[i][j],z[i][j]])
					aux=r.apply(aux)
					x[i][j]=aux[0]
					y[i][j]=aux[1]
					z[i][j]=aux[2]
		return [x,y,z]


	def draw_Orthohedron(self,fig):
		aux=self.points_Orthohedron()
		
		fig.set_xticks([np.amin(aux[0]),(np.amin(aux[0])+np.amax(aux[0]))/2,np.amax(aux[0])])
		fig.set_yticks([np.amin(aux[1]),(np.amin(aux[1])+np.amax(aux[1]))/2,np.amax(aux[1])])
		fig.set_zticks([np.amin(aux[2]),(np.amin(aux[2])+np.amax(aux[2]))/2,np.amax(aux[2])])
		fig.set_xlabel("X")
		fig.set_ylabel("Y")
		fig.set_zlabel("Z")
		fig.plot_surface(aux[0], aux[1], aux[2], color='b')

	def save(self,name):
		with open (name, 'wb') as output:
			pickle.dump(self,output)

	def load(self,name):
		with open (name, 'rb') as input:
			self=pickle.load(input)
		return self

class ODF:
	def __init__(self,type=0):
		self.type=type
		self.modes=[]
	##Type:
	#0-> powder, 1-> Flor, 2-> Fourrier, 3-> Monocrystalline
	# ODF save like -> [angle 1, angle 2,angle 3,weight, radius] 'zxz'
	def load_modes(self,modos):
		self.modes=modos

	def save(self,name):
		with open (name, 'wb') as output:
			pickle.dump(self,output)

	def load(self,name):
		with open (name, 'rb') as input:
			#self=pickle.load(input)
			aux=pickle.load(input)
			self.type=aux.type
			self.modes=aux.modes
		return self

class Last_step():
	def __init__(self):
		self.name=None
	def update(self,lststp):
		self.name=lststp

class NCrystal_file:
	def __init__(self,name,temp,lam):
		self.name=name
		self.temp=temp
		self.lam=lam
	def add_data(self,data):
		self.lam=data
	def save_Crystal_data(self):
		with open ("Aux.pkl",'wb') as output:
			pickle.dump(self,output)
	def load_Ncrystal_data(self):
		with open("Aux.pkl",'rb') as input:
			aux=pickle.load(input)
			self.name=aux.name
			self.temp=aux.temp
			self.lam=aux.lam

class N_Crystal_window_file:
	def __init__(self,name):
		self.name=name
		self.data=[]
		self.data2=[]
		self.elas_coh=[]
	def add_data(self,data1,data2,data3):
		self.data=data1
		self.data2=data2
		self.elas_coh=data3
	def save_data(self,name):
		with open(name, 'wb') as output:
			pickle.dump(self,output)
	def load_data(self,name):
		with open(name,'rb') as input:
			aux=pickle.load(input)
			self.name=aux.name 
			self.data=aux.data 
			self.data2=aux.data2
			self.elas_coh=aux.elas_coh

