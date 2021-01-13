import tkinter.ttk as ttk
import tkinter as tk
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import sys
import scipy.io


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


# This import_wizard was created to facilitate the user
# to import data corresponding to the cross section without Bragg-Component

# File types recommended are .odf .dat and .txt

# The user is allowed to define the data in each imported column


datos_finales=None   # This global variable will be used by the main code to obtain the rotations

def import_list(name):

	global datos_finales
	window_2= tk.Tk()
	window_2.geometry('400x300')
	window_2.resizable(0,0)
	window_2.title("Import_wizard")

# Matlab files tend have a rather complicated object list format
# The chances of reading the file correctly are almost 100%
# if the user knows the number of columns and rows
# In case the parameters are unknown to the user,
# a system was implemented in the function clk1()

	if name[-3:]=="mat":
		mat=scipy.io.loadmat(name)
		lbl1=tk.Label(window_2,text="Number of columns:",anchor=tk.W)
		lbl1.place(height=30,width=150,x=10,y=20)

		spn1 = tk.Spinbox(window_2, from_=0, to=20)
		spn1.place(height=30,width=50,x=150,y=20)

		def clk_ckb1():
			if ckvar1.get()==False:
				ckvar1.set(True)
			else:
				ckvar1.set(False)


		ckvar1=tk.BooleanVar()
		ckb1=ttk.Checkbutton(window_2,text="Unknow",command=clk_ckb1,variable=ckvar1)
		ckb1.place(height=30,width=80,x=210,y=20)
		ckvar1.set(False)

		lbl2=tk.Label(window_2,text="Number of rotations:",anchor=tk.W)
		lbl2.place(height=30,width=150,x=10,y=60)

		spn2 = tk.Spinbox(window_2, from_=0, to=100)
		spn2.place(height=30,width=50,x=150,y=60)

		def clk_ckb2():
			if ckvar2.get()==False:
				ckvar2.set(True)
			else:
				ckvar2.set(False)


		ckvar2=tk.BooleanVar()
		ckb2=ttk.Checkbutton(window_2,text="Unknow",command=clk_ckb2,variable=ckvar2)
		ckb2.place(height=30,width=80,x=210,y=60)
		ckvar2.set(False)


		# Ignore all arrangements of lenght 1
		# It is assumed that the number of rotations is read first
		# and then the number of columns
		def clk1():
			global datos
			cols=0
			num=0
			if ckvar1.get()==True and ckvar2.get()==True:
				aux=mat[list(mat.keys())[-1:][0]]
				while len(aux)==1:
					aux=aux[0]
				num=len(aux)
				cols=len(aux[0])
			if ckvar1.get()==True and ckvar2.get()==False:
				aux=mat[list(mat.keys())[-1:][0]]
				num=spn2.get()
				while len(aux)!=num:
					aux=aux[0]
				cols=len(aux[0])
			if ckvar1.get()==False and ckvar2.get()==True:
				aux=mat[list(mat.keys())[-1:][0]]
				cols=spn1.get()
				while len(aux[0])!=num:
					aux=aux[0]
				num=len(aux)
			if ckvar1.get()==False and ckvar2.get()==False:
				aux=mat[list(mat.keys())[-1:][0]]
				num=spn2.get()
				cols=spn1.get()
				while len(aux)!=num:
					aux=aux[0]
			datos=np.zeros((cols,num))
			for i in range (cols):
				for j in range (num):
					try:
						datos[i][j]=float(aux[j][i])
					except:
						datos[i][j]=0
			names=None
			import_list_2(cols,names,window_2,datos)

		btn1=tk.Button(window_2,text="Load",command=clk1,fg="red")
		btn1.place(height=60,width=80,x=310,y=20)


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
							datos[j][i-ignore]=float(s[j])
						except:
							messagebox.showinfo('Error: Invalid data','Invalid format data')
							return 0
				else:
					messagebox.showinfo('Error: Invalid data','Invalid data in line'+i)
					return 0


			import_list_2(aux,names,window_2,datos)


		btn1=tk.Button(window_2,text="Load",command=clk1,fg="red")
		btn1.place(height=80,width=80,x=310,y=20)


	window_2.mainloop()

#Once the user loads the data, it's necessary to identify the data in each column
#In case the information in the column is not relevant, 
#the user can leave his name blank or assign the option "other"

def import_list_2(num,names,window_2,datos):
	global datos_finales
	cols=('Columns','Information')
	names_cols=ttk.Treeview(window_2,columns=cols,show='headings')
	names_cols.place(height=150,width=180,x=10,y=130)
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

	lbl3=tk.Label(window_2,text="Information in \n column                 is:",anchor=tk.W)
	lbl3.place(height=60,width=180,x=190,y=110)

	spn2 = tk.Spinbox(window_2, from_=0, to=num-1)
	spn2.place(height=20,width=50,x=250,y=140)

	cmb2=ttk.Combobox(window_2, values=["Lambda","d-spacing","Cross section (CS)","Absorption (ABS)","Bragg component (BC)","CS -BC","CS -BC -ABS","other"])
	cmb2.place(height=25,width=140,x=190,y=165)
	cmb2.current(0)

	def clk2():
		col=spn2.get()
		names_cols.delete(col)
		names_cols.insert("","end",iid=col,values=(col,cmb2.get()))

	btn2=tk.Button(window_2,text="Set",command=clk2,fg="red")
	btn2.place(height=60,width=50,x=335,y=130)

	def clk3():
		global datos_finales
		datos_finales=np.zeros((2,datos.shape[1]))
		
		for i in range (num):
			if names_cols.item(i,option="values")[1]=="Lambda":
				datos_finales[0]=datos[i]
			if names_cols.item(i,option="values")[1]=="d-spacing":
				datos_finales[0]=2*np.array(datos[i])
			if names_cols.item(i,option="values")[1]=="Cross section (CS)":
				datos_finales[1]=datos[i]
			if names_cols.item(i,option="values")[1]=="Absorption (ABS)":
				datos_finales[1]+=np.array(datos[i])
			if names_cols.item(i,option="values")[1]=="CS -BC -ABS":
				datos_finales[1]+=np.array(datos[i])

	    
		window_2.quit()
		window_2.destroy()

	btn3=tk.Button(window_2,text="Finish",command=clk3,fg="red")
	btn3.place(height=60,width=100,x=260,y=220)

