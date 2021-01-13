import tkinter.ttk as ttk
import tkinter as tk
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import sys
import scipy.io
from scipy.spatial.transform import Rotation as R

modos=None
cmb1_var=None

def importar_modos(name):

	window_2= tk.Tk()

	window_2.geometry('400x380')
	window_2.resizable(0,0)
	window_2.title("Import_wizard")

	if name[-3:]=="mat":

		labels=[]
		mat=scipy.io.loadmat(name)
		for ii in mat.keys():
			if ii!="__header__" and ii!="__version__" and ii!="__globals__" and ii!="__function_workspace__":
				labels.append(ii)

		lbl1=tk.Label(window_2,text="One matlab file was selected:",anchor=tk.W)
		lbl1.place(height=30,width=200,x=10,y=20)

		radVar2=tk.IntVar()
		

		def clk_rad1():
			global cmb1_var
			def clk_cmb1(event):
				global cmb1_var
				cmb1_var=cmb1.get()
				print(cmb1_var)
			cmb1=ttk.Combobox(window_2, values=labels,state=tk.NORMAL)
			cmb1.bind("<<ComboboxSelected>>", clk_cmb1)
			cmb1.place(height=25,width=80,x=310,y=50)
			cmb1.current(0)
			cmb1_var=cmb1.get()
			radVar2.set(1)
		def clk_rad2():
			cmb1=ttk.Combobox(window_2, values=labels,state=tk.DISABLED)
			cmb1.place(height=25,width=80,x=310,y=50)
			cmb1.current(0)
			radVar2.set(2)

		rad1=tk.Radiobutton(window_2,text="the file contains the ODF, with the label:",variable=radVar2,value=1,command=clk_rad1,anchor=tk.W)
		rad1.place(height=30,width=300,x=10,y=50)

		rad2=tk.Radiobutton(window_2,text="the file contains a list of the main modes",variable=radVar2,value=2,command=clk_rad2,anchor=tk.W)
		rad2.place(height=30,width=250,x=10,y=80)
		radVar2.set(2)

		def clk1():
			global modos
			if radVar2.get()==1:
				datos=mat[cmb1_var]
				modos=np.zeros((5,len(datos[0][0][2])))
				try:
					for ii in range (0, len(datos[0][0][2])):
						if len(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][0])==1:
							modos[1][ii]=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][0][0][ii])
							modos[2][ii]=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][1][0][ii])
							modos[3][ii]=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][2][0][ii])
							modos[4][ii]=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][3][0][ii])
							modos[0][ii]=float(datos[0][0][2][ii][0])
						else:
							modos[1][ii]=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][0][ii][0])
							modos[2][ii]=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][1][ii][0])
							modos[3][ii]=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][2][ii][0])
							modos[4][ii]=float(datos[0][0][1][0][0][7][0][0][2][0][0][0][0][0][3][ii][0])
							modos[0][ii]=float(datos[0][0][2][ii][0])
				except:
					messagebox.showinfo('Error: Invalid data','Sorry, we can\'t read the format data, please search over allowed formats')
				modos=modos[:,modos[0].argsort()]
				modos=np.flip(modos, axis=1)
				#for ii in range (0, len(datos[0][0][2])):
				#	r = R.from_quat([modos[1][ii], modos[2][ii], modos[3][ii], modos[4][ii]])
				#	print(r.as_euler('zxz',degrees=True),modos[0][ii])
				window_2.quit()
				window_2.destroy()
			if radVar2.get()==2:
					aux=mat[list(mat.keys())[-1:][0]]
					while len(aux)==1:
						aux=aux[0]
					if len(aux)<20:
						num=np.zeros((len(aux),len(aux[0])))
						try:
							for i in range (len (aux)):
								for j in range (len (aux[0])):
									num[i][j]=float(aux[i][j])
						except:
							messagebox.showinfo('Error: Invalid data','Sorry, we can\'t read the format data, please search over allowed formats')
							window_2.quit()
							window_2.destroy()
					else:
						num=np.zeros((len(aux[0]),len(aux)))
						try:
							for i in range (len (aux)):
								for j in range (len (aux[0])):
									num[j][i]=float(aux[i][j])
						except:
							messagebox.showinfo('Error: Invalid data','Sorry, we can\'t read the format data, please search over allowed formats')
							window_2.quit()
							window_2.destroy()
					names=None
					import_modes_2(num,names,window_2_2)

		btn1=tk.Button(window_2,text="Load data",command=clk1,fg="red")
		btn1.place(height=40,width=120,x=10,y=110)
		
	else:

		lbl1=tk.Label(window_2,text="Ignore first                 lines",anchor=tk.W)
		lbl1.place(height=30,width=180,x=10,y=20)

		spn1 = tk.Spinbox(window_2, from_=0, to=10)
		spn1.place(height=30,width=50,x=90,y=20)

		lbl2=tk.Label(window_2,text="Separator:",anchor=tk.W)
		lbl2.place(height=30,width=80,x=10,y=50)

		cmb1=ttk.Combobox(window_2, values=["space","tab",";","&"])
		cmb1.place(height=30,width=70,x=90,y=50)
		cmb1.current(0)

		txt1=tk.Entry(window_2,text="",state=tk.DISABLED)
		txt1.place(height=30,width=50,x=240,y=50)

		ckvar2_1=tk.BooleanVar()

		def clk_ckb1():
			global txt1
			if ckvar2_1.get()==False:
				txt1=tk.Entry(window_2,text="",state=tk.NORMAL)
				txt1.place(height=30,width=50,x=240,y=50)
				ckvar2_1.set(True)
			else:
				txt1=tk.Entry(window_2,text="",state=tk.DISABLED)
				txt1.place(height=30,width=50,x=240,y=50)
				ckvar2_1.set(False)

		ckb1=ttk.Checkbutton(window_2,text="other:",command=clk_ckb1,variable=ckvar2_1)
		ckb1.place(height=30,width=60,x=170,y=50)
		ckvar2_1.set(False)

		def clk_ckb2():
			if ckvar2.get()==False:
				ckvar2.set(True)
			else:
				ckvar2.set(False)


		ckvar2=tk.BooleanVar()
		ckb2=ttk.Checkbutton(window_2,text="Use firt row as column names:",command=clk_ckb2,variable=ckvar2)
		ckb2.place(height=30,width=250,x=10,y=80)
		ckvar2.set(False)

		datos=None

		def clk1():
			global datos
			if ckvar2_1.get()==True:
				try:
					sep=txt1.get()
				except:
					messagebox.showinfo('Error: Invalid data','Invalid caracter for separator')
			else:
				if cmb1.get()=="space":
					sep=" "
				elif cmb1.get()=="tab":
					sep='\t'
				else:
					sep=cmb1.get()

			data=open(name,"r")
			lines=data.readlines()

			if ckvar2.get()==True:
				names=lines[0].strip().split(sep)
				ignore=int(spn1.get())+1
			else:
				names=None
				ignore=int(spn1.get())


			aux=len(lines[ignore+1].strip().split(sep))
			datos=np.zeros((aux,len(lines)-ignore))
			for i in range (ignore,len(lines)):
				s=lines[i].strip().split(sep)
				if len(s)==aux:
					for j in range (0,aux):
						try:
							datos[j][i-ignore]=s[j]
						except:
							print(s[j])
							messagebox.showinfo('Error: Invalid data','Invalid format data')
							return 0
				else:
					messagebox.showinfo('Error: Invalid data','Invalid data in line'+i)
					return 0

			
			import_modes_2(aux,datos,names,window_2)
		btn1=tk.Button(window_2,text="Load data",command=clk1,fg="red")
		btn1.place(height=40,width=120,x=10,y=110)

	window_2.mainloop()

def import_modes_2(num,datos, names,window_2):
	global modos
	cols=('Columns','Information')
	names_cols=ttk.Treeview(window_2,columns=cols,show='headings')
	names_cols.place(height=150,width=180,x=10,y=150)
	names_cols.column('Columns',width=90,minwidth=30)
	names_cols.column('Information',width=90,minwidth=30)
	for col in cols:
		names_cols.heading(col,text=col)
	if names!=None:
		for i in range (num):
			names_cols.insert("","end",iid=int(i),values=(i,names[i]))
	else:
		for i in range (num):
			names_cols.insert("","end",iid=int(i),values=(i,"-"))

	def clk_ckb3():
		if ckvar3.get()==False:
			ckvar3.set(True)
		else:
			ckvar3.set(False)


	ckvar3=tk.BooleanVar()
	ckb3=ttk.Checkbutton(window_2,text="use different radios:",command=clk_ckb3,variable=ckvar3)
	ckb3.place(height=30,width=250,x=10,y=310)
	ckvar3.set(False)


	lbl3=tk.Label(window_2,text="Information in \n column                 is:",anchor=tk.W)
	lbl3.place(height=60,width=180,x=190,y=110)

	spn2 = tk.Spinbox(window_2, from_=0, to=num-1)
	spn2.place(height=20,width=50,x=250,y=140)

	cmb2=ttk.Combobox(window_2, values=["quaternion-a","quaternion-b","quaternion-c","quaternion-d","[a b c d]","φ","θ","ψ","[φ θ ψ]","weight","radius","other"])
	cmb2.place(height=25,width=140,x=190,y=165)
	cmb2.current(0)

	def clk2():
		col=spn2.get()
		names_cols.delete(col)
		names_cols.insert("","end",iid=col,values=(col,cmb2.get()))

	btn2=tk.Button(window_2,text="Set",command=clk2,fg="red")
	btn2.place(height=60,width=50,x=335,y=130)

	def clk3():
		global modos
		if ckvar3.get()==False:

			modos=np.zeros((4,datos.shape[1]))
			
			for i in range(0,4):
				for j in range (datos.shape[1]):
					modos[i][j]=None

			for i in range (num):
				if names_cols.item(i,option="values")[1]=="weight":
					modos[0]=datos[i]
				if names_cols.item(i,option="values")[1]=="φ":
					modos[1]=datos[i]
				if names_cols.item(i,option="values")[1]=="θ":
					modos[2]=datos[i]
				if names_cols.item(i,option="values")[1]=="ψ":
					modos[3]=datos[i]
		else:
			modos=np.zeros((6,datos.shape[1]))
			
			for i in range(0,6):
				for j in range (datos.shape[1]):
					modos[i][j]=None

			for i in range (num):
				if names_cols.item(i,option="values")[1]=="weight":
					modos[0]=datos[i]
				if names_cols.item(i,option="values")[1]=="φ":
					modos[1]=datos[i]
				if names_cols.item(i,option="values")[1]=="θ":
					modos[2]=datos[i]
				if names_cols.item(i,option="values")[1]=="ψ":
					modos[3]=datos[i]
				if names_cols.item(i,option="values")[1]=="radius":
					modos[5]=datos[i]


	    
		window_2.quit()
		window_2.destroy()

	btn3=tk.Button(window_2,text="Finish",command=clk3,fg="red")
	btn3.place(height=60,width=100,x=260,y=220)

