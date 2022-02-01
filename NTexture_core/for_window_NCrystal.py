#!/usr/bin/env python
from __future__ import print_function
import project_class as cl
import NCrystal
import numpy as np
import matplotlib.pyplot as plt


elemt=('Ag_sg225.ncmat','Al_sg225.ncmat','Au_sg225.ncmat','Ba_sg229.ncmat','Be_sg194.ncmat','Bi.ncmat','Ca_sg225.ncmat','Ca_sg229_Calcium-gamma.ncmat','Cr_sg229.ncmat','C_sg194_pyrolytic_graphite.ncmat','C_sg227_Diamond.ncmat','Cu_sg225.ncmat','Fe_sg229_Iron-alpha.ncmat','Fe_sg229_Iron-beta.ncmat','Ge_sg227.ncmat','MgO_sg225_Periclase.ncmat','Mg_sg194.ncmat','Mo_sg229.ncmat','Na_sg229.ncmat','Nb_sg229.ncmat','Ni_sg225.ncmat','Pb_sg225.ncmat','Pd_sg225.ncmat','Pt_sg225.ncmat','Rb_sg229.ncmat','Sc_sg194.ncmat','Si_sg227.ncmat','Sn_sg141.ncmat','Sr_sg225.ncmat','Ti_sg194.ncmat','V_sg229.ncmat','W_sg229.ncmat','Y_sg194.ncmat','Zn_sg194.ncmat','Zr_sg194.ncmat')
#Na no more than 1620K

for name in elemt:
	print(name)
	direc="/home/chang/Desktop/NText_1.0/NCrystal/Instalacion/data/"+name

	aux=cl.N_Crystal_window_file(name.split('.')[0])


	data1=np.zeros((400,10))
	data2=np.zeros((400,10))
	aux2=[]

	for t,tt in enumerate(np.arange(5,1625,5)):
		print(tt)
		
		pc= NCrystal.createScatter(direc + ";dcutoff=0.1;bragg=false;temp="+str(tt)+"K")
		ab= NCrystal.createAbsorption(direc + ";dcutoff=0.1;temp="+str(tt)+"K")


		lam=np.linspace(0.5,5,num=200)

		aux1=[]

		for ii in lam:
			ekin=NCrystal.wl2ekin(ii)
			aux1.append(pc.crossSectionNonOriented(ekin)+ab.crossSectionNonOriented(ekin))
			

		parametros=np.polyfit(lam,aux1,9)
		np.flip(parametros)

		for i,ii in enumerate(parametros):
			data1[t][i]=float(ii)

		lam=np.linspace(5,20,num=200)

		aux1=[]

		for ii in lam:
			ekin=NCrystal.wl2ekin(ii)
			aux1.append(pc.crossSectionNonOriented(ekin)+ab.crossSectionNonOriented(ekin))

		parametros=np.polyfit(lam,aux1,9)
		np.flip(parametros)
		for i,ii in enumerate(parametros):
			data2[t][i]=float(ii)


	pc_b= NCrystal.createScatter(direc + ";dcutoff=0.1;bkgd=none;temp="+str(300)+"K")
	lam=np.linspace(0.5,10,num=1000)
	for ii in lam:
		ekin=NCrystal.wl2ekin(ii)
		aux2.append(pc_b.crossSectionNonOriented(ekin))
	aux2=np.array(aux2)
	aux.add_data(data1,data2,aux2)
	aux.save_data("NCrystal_window/"+str(name.split('.')[0])+".pkl")

		#(parametros[0]*jj**9+parametros[1]*jj**8+parametros[2]*jj**7+parametros[3]*jj**6+parametros[4]*jj**5+parametros[5]*jj**4+parametros[6]*jj**3+parametros[7]*jj**2+parametros[8]*jj**1+parametros[9]*jj**0)



