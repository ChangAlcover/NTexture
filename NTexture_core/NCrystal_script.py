#!/usr/bin/env python
from __future__ import print_function
import project_class as cl
import NCrystal
import numpy as np
import matplotlib.pyplot as plt

aux=cl.NCrystal_file("abc",[0],[0])
aux.load_Ncrystal_data()

pc_b= NCrystal.createScatter(aux.name + ";dcutoff=0.1;bkgd=none;temp="+str(aux.temp)+"K")
pc= NCrystal.createScatter(aux.name + ";dcutoff=0.1;bragg=false;temp="+str(aux.temp)+"K")
pc_t= NCrystal.createScatter(aux.name + ";dcutoff=0.1;temp="+str(aux.temp)+"K")
ab= NCrystal.createAbsorption(aux.name + ";dcutoff=0.1;temp="+str(aux.temp)+"K")

#plt.figure(aux.name.split('/')[-1].split('.')[0].split('_')[0])
x=[]
x2=[]
total=[]
absor=[]
Bragg=[]
Total_brag=[]

lam=aux.lam

aux1=[]
aux2=[]
aux3=[]
aux4=[]

for ii in lam:
	ekin=NCrystal.wl2ekin(ii)
	aux1.append(ii)
	aux2.append(ekin)
	aux3.append(pc.crossSectionNonOriented(ekin)+ab.crossSectionNonOriented(ekin))
	aux4.append(pc_b.crossSectionNonOriented(ekin))
aux.add_data([aux1,aux2,aux3,aux4])
aux.save_Crystal_data()


'''
if aux.data[1]==1:
	lam=np.linspace(aux.data[2],aux.data[3],num=200)
	for ii in lam:
		ekin=NCrystal.wl2ekin(ii)
		aux1=""
		x.append(ii)
		x2.append(ekin)
		if aux.data[4]:
			aux1+=str(ii)+"\t"
		if aux.data[5]:
			aux1+=str(ekin) +"\t"
		if aux.data[6]:
			aux1+=str(pc_t.crossSectionNonOriented(ekin)+ab.crossSectionNonOriented(ekin)) +"\t"
			total.append(pc_t.crossSectionNonOriented(ekin)+ab.crossSectionNonOriented(ekin))
		if aux.data[7]:
			aux1+=str(ab.crossSectionNonOriented(ekin)) +"\t"
			absor.append(ab.crossSectionNonOriented(ekin))
		if aux.data[8]:
			aux1+=str(pc_b.crossSectionNonOriented(ekin)) +"\t"
			Bragg.append(pc_b.crossSectionNonOriented(ekin))
		if aux.data[9]:
			aux1+=str(pc.crossSectionNonOriented(ekin)+ab.crossSectionNonOriented(ekin)) +"\t"
			Total_brag.append(pc.crossSectionNonOriented(ekin)+ab.crossSectionNonOriented(ekin))
		print(aux1)

else:
	lam=np.linspace(aux.data[2],aux.data[3],num=200)
	for ii in lam:
		la=NCrystal.ekin2wl(ii)
		aux1=""
		x2.append(la)
		x.append(ii)
		if aux.data[4]:
			aux1+=str(la)+"\t"
		if aux.data[5]:
			aux1+=str(ii) +"\t"
		if aux.data[6]:
			aux1+=str(pc_t.crossSectionNonOriented(ii)+ab.crossSectionNonOriented(ii)) +"\t"
			total.append(pc_t.crossSectionNonOriented(ii)+ab.crossSectionNonOriented(ii))
		if aux.data[7]:
			aux1+=str(ab.crossSectionNonOriented(ii)) +"\t"
			absor.append(ab.crossSectionNonOriented(ii))
		if aux.data[8]:
			aux1+=str(pc_b.crossSectionNonOriented(ii)) +"\t"
			Bragg.append(pc_b.crossSectionNonOriented(ii))
		if aux.data[9]:
			aux1+=str(pc.crossSectionNonOriented(ii)+ab.crossSectionNonOriented(ii)) +"\t"
			Total_brag.append(pc.crossSectionNonOriented(ii)+ab.crossSectionNonOriented(ii))
		print(aux1)


## Plotting code

plt.xscale('linear')
plt.xlabel('Wavelength [A]')
plt.ylabel('Cross sections [barns]')
if aux.data[6]:
	plt.plot(x,total,label="Total cross section")
if aux.data[7]:
	plt.plot(x,absor,label="Absorption cross section")
if aux.data[8]:
	plt.plot(x,Bragg,label="Bragg component (powder)")
if aux.data[9]:
	plt.plot(x,Total_brag,label="Total cross section without Bragg component")
plt.figure(aux.name.split('/')[-1].split('.')[0].split('_')[0]+"_energy")
plt.xscale('log')
plt.xlabel('Energy [eV]')
plt.ylabel('Cross sections [barns]')
if aux.data[6]:
	plt.plot(x2,total,label="Total cross section")
if aux.data[7]:
	plt.plot(x2,absor,label="Absorption cross section")
if aux.data[8]:
	plt.plot(x2,Bragg,label="Bragg component (powder)")
if aux.data[9]:
	plt.plot(x2,Total_brag,label="Total cross section without Bragg component")

plt.legend(loc='upper right')
plt.show()
'''