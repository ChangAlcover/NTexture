import numpy as np
import scipy.special as special
import pylab as pl
import quaternion as quat
from scipy.spatial.transform import Rotation as R
#import PSpincalc as sp
import time as tm
import Fs as fnc
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle 
import lmfit as lm

import Fs as fs
import import_wizard as wiz
import import_wizard_modes as wiz_modes
import import_wizard_trans as wiz_trans
import import_wizard_sec as wiz_sec

radius=6

a=1
b=1
c=1
alfa=90
beta=90
gamma=90

estructura=0
dir_hkl=0
modos=0
direcciones={}
beam=np.array([0,0,1])
neutron_path=None
transmision={}
sec_no_elas_coh=None
function_base={}
datos_ajuste=None
sec_powder=0
sec_no_elas=0

ND=np.array([0,0,1])
LD=np.array([0,1,0])
TD=np.array([1,0,0])

x=None
y=None
z=None
d=0

window= tk.Tk()
window.geometry('800x600')
window.resizable(0,0)
window.title("NTexture")

##Define the fundamental steps

aplicacion_1=tk.LabelFrame(window,text="Structure")
aplicacion_1.place(height=525,width=800,x=0,y=70)
aplicacion_3=tk.LabelFrame(window,text="Geometry")
aplicacion_3.place(height=525,width=800,x=0,y=70)
aplicacion_2=tk.LabelFrame(window,text="HKL list")
aplicacion_2.place(height=120,width=800,x=0,y=70)
aplicacion_4=tk.LabelFrame(window,text="Beam direction")
aplicacion_4.place(height=525,width=800,x=0,y=70)
aplicacion_5=tk.LabelFrame(window,text="Simulations")
aplicacion_5.place(height=415,width=800,x=0,y=180)
aplicacion_6=tk.LabelFrame(window,text="Adjust")
aplicacion_6.place(height=525,width=800,x=0,y=70)

aplicacion_top_1=tk.LabelFrame(window,text="Main steps")
aplicacion_top_1.place(height=70,width=550,x=0,y=0)

aplicacion_top_2=tk.LabelFrame(window,text="Extra resources")
aplicacion_top_2.place(height=70,width=250,x=550,y=0)


aplicacion_top_1.tkraise()
aplicacion_top_2.tkraise()

## Buttons to choose the step
def clk1():
	aplicacion_1.tkraise()
def clk2():
	aplicacion_3.tkraise()
def clk3():
	aplicacion_2.tkraise()
	aplicacion_5.tkraise()
def clk3_1():
	aplicacion_4.tkraise()
def clk1_1():
	aplicacion_6.tkraise()
	aplicacion_6_raise()
btn1=tk.Button(aplicacion_top_2, text="Generate\n strucuture", command=clk1,anchor=tk.W,highlightcolor="red")
btn1_1=tk.Button(aplicacion_top_2, text="Adjust\n function", command=clk1_1,anchor=tk.W,highlightcolor="red")
btn2=tk.Button(aplicacion_top_1, text="Geometry", command=clk2,anchor=tk.W,highlightcolor="red")
btn3=tk.Button(aplicacion_top_1, text="Simulations", command=clk3,anchor=tk.W,highlightcolor="red")
btn3_1=tk.Button(aplicacion_top_1, text="Beam", command=clk3_1,anchor=tk.W,highlightcolor="red")

btn1.place(height=45, width=90,y=0,x=20)
btn1_1.place(height=45, width=90,y=0,x=130)

btn2.place(height=30, width=140,y=5,x=20)
btn3.place(height=30, width=140,y=5,x=340)
btn3_1.place(height=30, width=140,y=5,x=180)

def Geometry_help(event):
	tk.messagebox.showinfo(title="Step Info", message="In the seccion \"Geometry\" the user can:\n -Use one of the supplied geometries and define the center of it\n -move and rotate the figure\n -save and load the geommetry\n -specify the orientation of principal direction\n \n★If the user just want the Bragg component of the cross section, skip this step")

def Beam_help(event):
	tk.messagebox.showinfo(title="Step Info",message="In the section \"Beam\" the user can:\n -Define the beam direction in different reference systems \n -then, the user need to define the rotation performed in the experiment \n -save and load the rotation list \n ★An import wizard was made to help the user import a list of rotation \n ★This step is required")

def Cross_s_help(event):
	tk.messagebox.showinfo(title="Step Info",message="★Before this step, the user must have defined the ratation list\n ★The first thing to do in this step should be load de \"Structure file\" and generate or load the \"hkl list\"\n ")

def Structure_help(event):
	tk.messagebox.showinfo(title="Create strucuture info",message="Tengo que poner algo aca, eventualmente")

btn2.bind("<Button-3>",Geometry_help)
btn3_1.bind("<Button-3>",Beam_help)
btn3.bind("<Button-3>",Cross_s_help)
btn1.bind("<Button-3>",Structure_help)

var_aux_1=tk.StringVar()
var_aux_2=tk.StringVar()
var_aux_modes=tk.StringVar()
var_aux_weigth=tk.StringVar()


def clk_rad4():
	global radm3, radm4,spn3,spn4,radVar4
	aux=0
	list_aux=[]
	for i in range (modos.shape[1]):
		aux+=modos[0][i]
		list_aux.append(aux)
	def link_weight_3():
		var_aux_weigth.set(list_aux[int(var_aux_modes.get())])
	def link_weight_4():
		var_aux_modes.set(list_aux.index(float(var_aux_weigth.get())))


	if radVar4.get()==1:
		radm3=tk.Radiobutton(aplicacion_5,text="mode number:",variable=radVar4,value=3,command=clk_rad4,anchor=tk.W,state=tk.DISABLED)
		radm3.place(height=30,width=30,x=560,y=280)
		radm4=tk.Radiobutton(aplicacion_5,text="weigth in modes:: ",variable=radVar4,value=4,command=clk_rad4,anchor=tk.W,state=tk.DISABLED)
		radm4.place(height=30,width=30,x=560,y=310)
		spn3 = tk.Spinbox(aplicacion_5, from_=0, to=modos.shape[1],textvariable=var_aux_modes,state=tk.DISABLED,command=link_weight_3)
		spn3.place(height=30,width=70,x=720,y=280)
		spn4 = tk.Spinbox(aplicacion_5, values=tuple(list_aux),textvariable=var_aux_weigth,state=tk.DISABLED,command=link_weight_4)
		spn4.place(height=30,width=70,x=720,y=310)
	if radVar4.get()==2:
		radm3=tk.Radiobutton(aplicacion_5,text="mode number:",variable=radVar4,value=3,command=clk_rad4,anchor=tk.W,state=tk.NORMAL)
		radm3.place(height=30,width=300,x=560,y=280)
		radm4=tk.Radiobutton(aplicacion_5,text="weigth in modes:: ",variable=radVar4,value=4,command=clk_rad4,anchor=tk.W,state=tk.NORMAL)
		radm4.place(height=30,width=300,x=560,y=310)
		spn3 = tk.Spinbox(aplicacion_5, from_=0, to=modos.shape[1],textvariable=var_aux_modes,state=tk.NORMAL,command=link_weight_3)
		spn3.place(height=30,width=70,x=720,y=280)
		spn4 = tk.Spinbox(aplicacion_5, values=tuple(list_aux),textvariable=var_aux_weigth,state=tk.NORMAL,command=link_weight_4)
		spn4.place(height=30,width=70,x=720,y=310)
		radVar4.set(3)
	if radVar4.get()==3:
		spn3 = tk.Spinbox(aplicacion_5, from_=0, to=modos.shape[1],textvariable=var_aux_modes,state=tk.NORMAL,command=link_weight_3)
		spn3.place(height=30,width=70,x=720,y=280)
		spn4 = tk.Spinbox(aplicacion_5, values=tuple(list_aux),textvariable=var_aux_weigth,state=tk.NORMAL,command=link_weight_4)
		spn4.place(height=30,width=70,x=720,y=310)
	if radVar4.get()==4:
		spn3 = tk.Spinbox(aplicacion_5, from_=0, to=modos.shape[1],textvariable=var_aux_modes,state=tk.NORMAL,command=link_weight_3)
		spn3.place(height=30,width=70,x=720,y=280)
		spn4 = tk.Spinbox(aplicacion_5, values=tuple(list_aux),textvariable=var_aux_weigth,state=tk.NORMAL,command=link_weight_4)
		spn4.place(height=30,width=70,x=720,y=310)	
	

radVar4=tk.IntVar() #To know if is all the modes will be used

def almost_run():
	global var_aux_1,var_aux_2, radVar4
	lbl22=tk.Label(aplicacion_5,text="Texture loaded with success",anchor=tk.W)
	lbl22.place(height=30,width=200,x=130,y=100)
	if len(direcciones.keys())==0:
		messagebox.showinfo('Error: One step incomplete','No rotations loaded')
		return 0

	lbl23=tk.Label(aplicacion_5,text=str(len(direcciones.keys()))+" rotation directions have been loaded",anchor=tk.W)
	lbl23.place(height=30,width=280,x=460,y=150)
	lbl24=tk.Label(aplicacion_5,text="Simulate from:                to:",anchor=tk.W)
	lbl24.place(height=30,width=200,x=460,y=180)
	lbl25=tk.Label(aplicacion_5,text="Please note that the simulation may take time", fg="red",anchor=tk.W)
	lbl25.place(height=30,width=320,x=260,y=360)

	spn1 = tk.Spinbox(aplicacion_5, from_=0, to=len(direcciones.keys()),textvariable=var_aux_1)
	spn1.place(height=30,width=50,x=570,y=180)
	var_aux_1.set("0")
	spn2 = tk.Spinbox(aplicacion_5, from_=0, to=len(direcciones.keys()),textvariable=var_aux_2)
	spn2.place(height=30,width=50,x=650,y=180)
	var_aux_2.set(str(len(direcciones.keys())))

	lbl23_2=tk.Label(aplicacion_5,text="The texture loaded have " +str(modos.shape[1])+" modes:",anchor=tk.W)
	lbl23_2.place(height=30,width=250,x=460,y=220)


	radm1=tk.Radiobutton(aplicacion_5,text="Use all the modes",variable=radVar4,value=1,command=clk_rad4,anchor=tk.W)
	radm1.place(height=30,width=150,x=460,y=250)

	radm2=tk.Radiobutton(aplicacion_5,text="Use until: ",variable=radVar4,value=2,command=clk_rad4,anchor=tk.W)
	radm2.place(height=30,width=100,x=460,y=280)

	radm3=tk.Radiobutton(aplicacion_5,text="mode number:",variable=radVar4,value=3,command=clk_rad4,anchor=tk.W,state=tk.DISABLED)
	radm3.place(height=30,width=100,x=560,y=280)

	radm4=tk.Radiobutton(aplicacion_5,text="weigth in modes:: ",variable=radVar4,value=4,command=clk_rad4,anchor=tk.W,state=tk.DISABLED)
	radm4.place(height=30,width=100,x=560,y=310)

	radVar4.set(1)




### A partir de aca la aplicacion para crear la estructura ###

lbl2=tk.Label(aplicacion_1,text="a:",anchor=tk.W)
lbl2.place(height=30,width=15,x=10,y=60)
lbl3=tk.Label(aplicacion_1,text="b:",anchor=tk.W)
lbl3.place(height=30,width=15,x=75,y=60)
lbl4=tk.Label(aplicacion_1,text="c:",anchor=tk.W)
lbl4.place(height=30,width=15,x=140,y=60)
lbl5=tk.Label(aplicacion_1,text="α:",anchor=tk.W)
lbl5.place(height=30,width=15,x=200,y=60)
lbl6=tk.Label(aplicacion_1,text="ß:",anchor=tk.W)
lbl6.place(height=30,width=15,x=260,y=60)
lbl7=tk.Label(aplicacion_1,text="γ:",anchor=tk.W)
lbl7.place(height=30,width=15,x=320,y=60)

txt1=tk.Entry(aplicacion_1,text="")
txt1.place(height=30,width=35,x=30,y=60)
txt2=tk.Entry(aplicacion_1,text="")
txt2.place(height=30,width=35,x=90,y=60)
txt3=tk.Entry(aplicacion_1,text="")
txt3.place(height=30,width=35,x=160,y=60)
txt4=tk.Entry(aplicacion_1,text="")
txt4.place(height=30,width=35,x=220,y=60)
txt5=tk.Entry(aplicacion_1,text="")
txt5.place(height=30,width=35,x=280,y=60)
txt6=tk.Entry(aplicacion_1,text="")
txt6.place(height=30,width=35,x=340,y=60)


def clk_cmb1(event):
	#global txt1,txt2,txt3,txt4,txt5,txt6,lbl7,lbl2,lbl3,lbl4,lbl5,lbl6
	lbl2.place(height=0,width=0,x=0,y=0)
	lbl3.place(height=0,width=0,x=0,y=0)
	lbl4.place(height=0,width=0,x=0,y=0)
	lbl5.place(height=0,width=0,x=0,y=0)
	lbl6.place(height=0,width=0,x=0,y=0)
	lbl7.place(height=0,width=0,x=0,y=0)

	txt1.place(height=0,width=0,x=0,y=0)
	txt2.place(height=0,width=0,x=0,y=0)
	txt3.place(height=0,width=0,x=0,y=0)
	txt4.place(height=0,width=0,x=0,y=0)
	txt5.place(height=0,width=0,x=0,y=0)
	txt6.place(height=0,width=0,x=0,y=0)
	if cmb1.get()=="Cubica":
		lbl2.place(height=30,width=10,x=10,y=60)
		txt1.place(height=30,width=35,x=30,y=60)
	elif cmb1.get()=="Tetragonal":
		lbl2.place(height=30,width=10,x=10,y=60)
		txt1.place(height=30,width=35,x=30,y=60)
		lbl4.place(height=30,width=15,x=75,y=60)
		txt3.place(height=30,width=35,x=90,y=60)
	elif cmb1.get()=="Ortorombica":
		lbl2.place(height=30,width=15,x=10,y=60)
		txt1.place(height=30,width=35,x=30,y=60)
		lbl3.place(height=30,width=15,x=75,y=60)
		txt2.place(height=30,width=35,x=90,y=60)
		lbl4.place(height=30,width=15,x=140,y=60)
		txt3.place(height=30,width=35,x=160,y=60)
	elif cmb1.get()=="Trigonal":
		lbl2.place(height=30,width=15,x=10,y=60)
		txt1.place(height=30,width=35,x=30,y=60)
		lbl5.place(height=30,width=15,x=75,y=60)
		txt4.place(height=30,width=35,x=90,y=60)
		lbl7.place(height=30,width=15,x=140,y=60)
		txt6.place(height=30,width=35,x=160,y=60)
	elif cmb1.get()=="Monoclinica":
		lbl2.place(height=30,width=15,x=10,y=60)
		txt1.place(height=30,width=35,x=30,y=60)
		lbl3.place(height=30,width=15,x=75,y=60)
		txt2.place(height=30,width=35,x=90,y=60)
		lbl4.place(height=30,width=15,x=140,y=60)
		txt3.place(height=30,width=35,x=160,y=60)
		lbl5.place(height=30,width=15,x=200,y=60)
		txt4.place(height=30,width=35,x=220,y=60)
	elif cmb1.get()=="Triclinica":
		lbl2.place(height=30,width=15,x=10,y=60)
		txt1.place(height=30,width=35,x=30,y=60)
		lbl3.place(height=30,width=15,x=75,y=60)
		txt2.place(height=30,width=35,x=90,y=60)
		lbl4.place(height=30,width=15,x=140,y=60)
		txt3.place(height=30,width=35,x=160,y=60)
		lbl5.place(height=30,width=15,x=200,y=60)
		txt4.place(height=30,width=35,x=220,y=60)
		lbl6.place(height=30,width=15,x=260,y=60)
		txt5.place(height=30,width=35,x=280,y=60)
		lbl7.place(height=30,width=15,x=320,y=60)
		txt6.place(height=30,width=35,x=340,y=60)
	elif cmb1.get()=="Hexagonal":
		lbl2.place(height=30,width=15,x=10,y=60)
		txt1.place(height=30,width=35,x=30,y=60)
		lbl3.place(height=30,width=15,x=75,y=60)
		txt2.place(height=30,width=35,x=90,y=60)
		lbl4.place(height=30,width=15,x=140,y=60)
		txt3.place(height=30,width=35,x=160,y=60)

def clk4():
	a=1


lbl1=tk.Label(aplicacion_1,text="Tipo de estructura:",anchor=tk.W)
lbl1.place(height=30,width=120,x=10,y=20)

cmb1=ttk.Combobox(aplicacion_1, values=["Cubica","Tetragonal","Ortorombica","Trigonal","Monoclinica","Triclinica","Hexagonal"])
cmb1.bind("<<ComboboxSelected>>", clk_cmb1)
cmb1.place(height=30,width=100,x=140,y=20)
cmb1.current(5)


lbl8=tk.Label(aplicacion_1,text="Nuevo atomo:",anchor=tk.W)
lbl8.place(height=30,width=120,x=10,y=110)

lbl10=tk.Label(aplicacion_1,text="Posiciones de Wickoff", anchor=tk.W)
lbl10.place(height=30,width=200,x=10,y=150)

lbl11=tk.Label(aplicacion_1,text="b", anchor=tk.W)
lbl11.place(height=30,width=30,x=220,y=150)

lbl12=tk.Label(aplicacion_1,text="Algo 2", anchor=tk.W)
lbl12.place(height=30,width=50,x=300,y=150)

txt10=tk.Entry(aplicacion_1,text="")
txt10.place(height=30,width=50,x=10,y=200)

txt11=tk.Entry(aplicacion_1,text="")
txt11.place(height=30,width=50,x=80,y=200)

txt12=tk.Entry(aplicacion_1,text="")
txt12.place(height=30,width=50,x=150,y=200)

txt13=tk.Entry(aplicacion_1,text="")
txt13.place(height=30,width=70,x=220,y=200)

txt14=tk.Entry(aplicacion_1,text="")
txt14.place(height=30,width=70,x=300,y=200)

btn4=tk.Button(aplicacion_1, text="Agregar", command=clk4,anchor=tk.W)
btn4.place(height=30, width=70,y=200,x=390)



## A partir de aca la parte de Simular la seccion eficaz

def clk10():
	global lbl20,a,b,c,gamma,alfa,beta,estructura
	dir1=filedialog.askopenfilename(title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
	try:
		estructura=fs.read(dir1)
		a=fs.a
		b=fs.b 
		c=fs.c 
		alfa=fs.alfa
		beta=fs.beta
		gamma=fs.gamma
		lbl20=tk.Label(aplicacion_2,text="The structure was loaded successfully",anchor=tk.W)
		lbl20.place(height=30,width=250,x=10,y=10)
	except:
		messagebox.showinfo('Error: Invalid file','Please, make sure the correct file was chosen. In case of doubts about the format, use the built-in tool')

def clk11():
	global dir_hkl,lbl21
	if estructura==0:
		messagebox.showinfo('Error: Structure needed','Please, load first the structure file')
		return
	fs.Crear_archivo(estructura)
	dir_hkl="Lista_hkl.txt"
	lbl21=tk.Label(aplicacion_2,text="The hkl list was created successfully",anchor=tk.W)
	lbl21.place(height=30,width=250,x=10,y=50)

def clk12():
	global dir_hkl,lbl21
	dir_hkl=filedialog.askopenfilename(title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
	lbl21=tk.Label(aplicacion_2,text="hkl list was successfully loaded",anchor=tk.W)
	lbl21.place(height=30,width=250,x=10,y=50)

lbl20=tk.Label(aplicacion_2,text="Structure needs to be loaded",fg="red",anchor=tk.W)
lbl20.place(height=30,width=200,x=10,y=10)

btn10=tk.Button(aplicacion_2,text="Load",command=clk10)
btn10.place(height=30,width=60,x=280,y=10)

def load_structure_help(event):
	tk.messagebox.showinfo(title="Load structure info",message="The Structure files should have:\n -One line with the cristalografic data (sides and angles)\n -Others lines should have the wickoff position of every atoms, the scaterring length and the value u^2\n -The user can create the files with the help of the extra resource \"Generate strucutre\"")

btn10.bind("<Button-3>",load_structure_help)

btn11=tk.Button(aplicacion_2,text="Generate hkl list",command=clk11)
btn11.place(height=30,width=150,x=250,y=50)

btn12=tk.Button(aplicacion_2,text="Load hkl list",command=clk12)
btn12.place(height=30,width=150,x=430,y=50)

lbl21=tk.Label(aplicacion_2,text="hkl list needed",fg="red",anchor=tk.W)
lbl21.place(height=30,width=100,x=10,y=50)


# def clk13():
# 	try:
# 		res=int(txt20.get())
# 		if res<0:
# 			res=res*(-1)
# 	except:
# 		messagebox.showinfo('Error: Invalid data','Please, the resolution must be a number')
# 	fs.Crear_uniforme(res)
# 	fs.Funcion_modos(Beam)

radVar1=tk.IntVar() #To select dust or textured material

def clk14():
	global modos
	name=filedialog.askopenfilename(title = "Select file",filetypes = (("MatLab files","*.mat"),("data files","*.dat"),("text files","*.txt"),("all files","*.*")))
	wiz_modes.importar_modos(name)
	modos=wiz_modes.modos
	try:
		modos[0]
		almost_run()
	except:
		asfd=1
		#Que no se me olvide poner un error por aca
def clk_rad1():
	if radVar1.get()==1:
		txt20=tk.Entry(aplicacion_5,state=tk.NORMAL)
		txt20.insert(0, "6")
		txt20.place(height=30,width=40,x=250,y=10)
		btn14=tk.Button(aplicacion_5,text="Load texture",command=clk14,state=tk.DISABLED)
		btn14.place(height=30,width=100,x=10,y=100)
	else:
		txt20=tk.Entry(aplicacion_5,state=tk.DISABLED)
		txt20.place(height=30,width=40,x=250,y=10)
		btn14=tk.Button(aplicacion_5,text="Load texture",command=clk14,state=tk.NORMAL)
		btn14.place(height=30,width=100,x=10,y=100)

rad1=tk.Radiobutton(aplicacion_5,text="Simulate powder with resolution:              degrees",variable=radVar1,value=1,command=clk_rad1,anchor=tk.W)
rad1.place(height=30,width=350,x=10,y=10)

rad2=tk.Radiobutton(aplicacion_5,text="Simulate a textured material",variable=radVar1,value=2,command=clk_rad1,anchor=tk.W)
rad2.place(height=30,width=250,x=10,y=40)
radVar1.set(2)

txt20=tk.Entry(aplicacion_5,state=tk.DISABLED)
txt20.place(height=30,width=40,x=250,y=10)

btn14=tk.Button(aplicacion_5,text="Load texture",command=clk14,state=tk.NORMAL)
btn14.place(height=30,width=100,x=10,y=100)





def clk15():
	a=1

btn15=tk.Button(aplicacion_2,text="Simular seccion eficaz",command=clk15)
btn15.place(height=30,width=150,x=250,y=250)

radVar2=tk.IntVar() #Instrument

lbls1=tk.Label(aplicacion_5,text="Instrument used:",anchor=tk.W)
lbls1.place(height=30,width=150,x=400,y=10)

def clkrad_2():
	if radVar2.get()==3:
		btns1=tk.Button(aplicacion_5,text="Load",command=clks1,state=tk.NORMAL)
		btns1.place(height=30,width=50,x=600,y=100)
	else:
		btns1=tk.Button(aplicacion_5,text="Load",command=clks1,state=tk.DISABLED)
		btns1.place(height=30,width=50,x=600,y=100)



rad3=tk.Radiobutton(aplicacion_5,text="ENGINX",variable=radVar2,value=1,anchor=tk.W,command=clkrad_2)
rad3.place(height=30,width=100,x=400,y=40)

rad4=tk.Radiobutton(aplicacion_5,text="IMAT",variable=radVar2,value=2,anchor=tk.W,command=clkrad_2)
rad4.place(height=30,width=100,x=400,y=70)

rad3=tk.Radiobutton(aplicacion_5,text="Insert a new instrument",variable=radVar2,value=3,anchor=tk.W,command=clkrad_2)
rad3.place(height=30,width=200,x=400,y=100)

radVar2.set(1)

def clks1():
	a=1

btns1=tk.Button(aplicacion_5,text="Load",command=clks1,state=tk.DISABLED)
btns1.place(height=30,width=50,x=600,y=100)

#More of the simulation step at the end

##Geometry section


def cylinder (r,h):
	u = np.linspace(0, 2 * np.pi, 100)
	H=np.linspace(0,h,100)
	R=np.linspace(0,r,100)
	x_1=r*np.outer(np.cos(u),np.ones(100))
	y_1=r*np.outer(np.sin(u),np.ones(100))
	z_1= np.outer(np.ones(100), H)

	x_2=np.outer(np.cos(u),R)
	y_2=np.outer(np.sin(u),R)
	z_2=np.outer(np.ones(100),h*np.ones(100))


	x_3=np.outer(np.cos(u),R)
	y_3=np.outer(np.sin(u),R)
	z_3=np.outer(np.ones(100),np.zeros(100))

	x=np.concatenate((x_1,x_2,x_3),axis=0)
	y=np.concatenate((y_1,y_2,y_3),axis=0)
	z=np.concatenate((z_1,z_2,z_3),axis=0)

	return x,y,z
	
	#ax.set_xticks([np.amin(x),(np.amin(x)+np.amax(x))/2,np.amax(x)])
	#ax.set_yticks([np.amin(y),(np.amin(y)+np.amax(y))/2,np.amax(y)])
	#ax.set_zticks([np.amin(z),(np.amin(z)+np.amax(z))/2,np.amax(z)])
	#ax.set_xlabel("X")
	#ax.set_ylabel("Y")
	#ax.set_zlabel("Z")
	#ax.plot_surface(x, y, z, color='b')

def sphere(r):
	u=np.linspace(0,2*np.pi,100)
	v=np.linspace(0,np.pi,100)
	x=r*np.outer(np.cos(u),np.sin(v))
	y=r*np.outer(np.sin(u),np.sin(v))
	z=r*np.outer(np.ones(100),np.cos(v))
	return x,y,z
	#ax.set_xticks([np.amin(x),(np.amin(x)+np.amax(x))/2,np.amax(x)])
	#ax.set_yticks([np.amin(y),(np.amin(y)+np.amax(y))/2,np.amax(y)])
	#ax.set_zticks([np.amin(z),(np.amin(z)+np.amax(z))/2,np.amax(z)])
	#ax.set_xlabel("X")
	#ax.set_ylabel("Y")
	#ax.set_zlabel("Z")
	#ax.plot_surface(x, y, z, color='b')

def cone(r,h):
	u = np.linspace(0, 2 * np.pi, 100)
	H=np.linspace(0,h,100)
	R=np.linspace(0,r,100)
	x_1=r*np.outer(np.cos(u),np.flip(H)/h)
	y_1=r*np.outer(np.sin(u),np.flip(H)/h)
	z_1= np.outer(np.ones(np.size(u)), H)

	x_2=np.outer(np.cos(u),R)
	y_2=np.outer(np.sin(u),R)
	z_2=np.outer(np.ones(100),np.zeros(100))

	x=np.concatenate((x_1,x_2),axis=0)
	y=np.concatenate((y_1,y_2),axis=0)
	z=np.concatenate((z_1,z_2),axis=0)
	return x,y,z

	#ax.set_xticks([np.amin(x),(np.amin(x)+np.amax(x))/2,np.amax(x)])
	#ax.set_yticks([np.amin(y),(np.amin(y)+np.amax(y))/2,np.amax(y)])
	#ax.set_zticks([np.amin(z),(np.amin(z)+np.amax(z))/2,np.amax(z)])
	#ax.set_xlabel("X")
	#ax.set_ylabel("Y")
	#ax.set_zlabel("Z")
	#ax.plot_surface(x, y, z, color='b')

def orthohedron(a,b,c):
	A=np.linspace(0,a,200)
	B=np.linspace(0,b,200)
	C=np.linspace(0,c,200)

	x_1=np.outer(np.ones(200),0*np.ones(200))
	y_1=np.outer(B,np.ones(200))
	z_1=np.outer(np.ones(200),C)

	x_2=np.outer(np.ones(200),a*np.ones(200))
	y_2=np.outer(B,np.ones(200))
	z_2=np.outer(np.ones(200),C)

	x_3=np.outer(np.ones(200),A)
	y_3=np.outer(np.ones(200),0*np.ones(200))
	z_3=np.outer(C,np.ones(200))

	x_4=np.outer(np.ones(200),A)
	y_4=np.outer(np.ones(200),b*np.ones(200))
	z_4=np.outer(C,np.ones(200))

	x_5=np.outer(A,np.ones(200))
	y_5=np.outer(np.ones(200),B)
	z_5=np.outer(np.ones(200),0*np.ones(200))

	x_6=np.outer(A,np.ones(200))
	y_6=np.outer(np.ones(200),B)
	z_6=np.outer(np.ones(200),c*np.ones(200))

	x=np.concatenate((x_1,x_2,x_3,x_4,x_5,x_6),axis=0)
	y=np.concatenate((y_1,y_2,y_3,y_4,y_5,y_6),axis=0)
	z=np.concatenate((z_1,z_2,z_3,z_4,z_5,z_6),axis=0)

	return x,y,z

	#ax.set_xticks([np.amin(x),(np.amin(x)+np.amax(x))/2,np.amax(x)])
	#ax.set_yticks([np.amin(y),(np.amin(y)+np.amax(y))/2,np.amax(y)])
	#ax.set_zticks([np.amin(z),(np.amin(z)+np.amax(z))/2,np.amax(z)])
	#ax.set_xlabel("X")
	#x.set_ylabel("Y")
	#ax.set_zlabel("Z")
	#ax.plot_surface(x, y, z, color='b')

	



	



lbl32=tk.Label(aplicacion_3,text="a:",anchor=tk.W)
lbl32.place(height=0,width=0,x=0,y=0)
lbl33=tk.Label(aplicacion_3,text="b:",anchor=tk.W)
lbl33.place(height=0,width=0,x=0,y=0)
lbl34=tk.Label(aplicacion_3,text="c:",anchor=tk.W)
lbl34.place(height=0,width=0,x=0,y=0)
lbl35=tk.Label(aplicacion_3,text="r:",anchor=tk.W)
lbl35.place(height=30,width=15,x=10,y=60)
lbl36=tk.Label(aplicacion_3,text="h:",anchor=tk.W)
lbl36.place(height=30,width=15,x=105,y=60)

txt31=tk.Entry(aplicacion_3,text="")
txt31.place(height=30,width=65,x=30,y=60)
txt32=tk.Entry(aplicacion_3,text="")
txt32.place(height=30,width=65,x=130,y=60)
txt33=tk.Entry(aplicacion_3,text="")
txt33.place(height=0,width=0,x=0,y=0)

lbl37=tk.Label(aplicacion_3,text="Base center coordinates:",anchor=tk.W)
lbl37.place(height=30,width=180,x=10,y=90)

lbl38=tk.Label(aplicacion_3,text="x:",anchor=tk.W)
lbl38.place(height=30,width=15,x=10,y=120)
lbl39=tk.Label(aplicacion_3,text="y:",anchor=tk.W)
lbl39.place(height=30,width=15,x=105,y=120)
lbl40=tk.Label(aplicacion_3,text="z:",anchor=tk.W)
lbl40.place(height=30,width=15,x=200,y=120)

txt35=tk.Entry(aplicacion_3,text="")
txt35.place(height=30,width=65,x=30,y=120)
txt36=tk.Entry(aplicacion_3,text="")
txt36.place(height=30,width=65,x=130,y=120)
txt37=tk.Entry(aplicacion_3,text="")
txt37.place(height=30,width=65,x=220,y=120)


def clk_cmb20(event):
	global lbl37,txt31,txt32,txt33,RD,LD,TD
	RD=np.array([1,0,0])
	LD=np.array([0,1,0])
	TD=np.array([0,0,1])
	lbl32.place(height=0,width=0,x=0,y=0)
	lbl33.place(height=0,width=0,x=0,y=0)
	lbl34.place(height=0,width=0,x=0,y=0)
	lbl35.place(height=0,width=0,x=0,y=0)
	lbl36.place(height=0,width=0,x=0,y=0)

	txt31.place(height=0,width=0,x=0,y=0)
	txt32.place(height=0,width=0,x=0,y=0)
	txt33.place(height=0,width=0,x=0,y=0)
	if cmb20.get()=="cone" or cmb20.get()=="cylinder":
		lbl35.place(height=30,width=15,x=10,y=60)
		lbl36.place(height=30,width=15,x=105,y=60)
		txt31.place(height=30,width=65,x=30,y=60)
		txt32.place(height=30,width=65,x=130,y=60)
		lbl37=tk.Label(aplicacion_3,text="Base center coordinates:",anchor=tk.W)
		lbl37.place(height=30,width=180,x=10,y=90)		
	if cmb20.get()=="sphere":
		lbl35.place(height=30,width=15,x=10,y=60)
		txt31.place(height=30,width=65,x=30,y=60)
		lbl37=tk.Label(aplicacion_3,text="Center coordinates:",anchor=tk.W)
		lbl37.place(height=30,width=180,x=10,y=90)
	if cmb20.get()=="orthohedron":
		lbl37=tk.Label(aplicacion_3,text="Vertices coordinates:",anchor=tk.W)
		lbl37.place(height=30,width=180,x=10,y=90)
		lbl32.place(height=30,width=15,x=10,y=60)
		lbl33.place(height=30,width=15,x=105,y=60)
		lbl34.place(height=30,width=15,x=200,y=60)
		txt31.place(height=30,width=65,x=30,y=60)
		txt32.place(height=30,width=65,x=130,y=60)
		txt33.place(height=30,width=65,x=220,y=60)

	

cmb20=ttk.Combobox(aplicacion_3, values=["cone","cylinder","sphere","orthohedron"])
cmb20.bind("<<ComboboxSelected>>", clk_cmb20)
cmb20.place(height=30,width=200,x=20,y=10)
cmb20.current(1)

lbl29=tk.Label(aplicacion_3,text="distance in [cm]",anchor=tk.W)
lbl29.place(height=30,width=120,x=230,y=10)


def clk30():
	global x,y,z,d
	d=1
	figure=plt.Figure(figsize=(6,5),dpi=100)
	bar1=FigureCanvasTkAgg(figure,aplicacion_3)
	bar1.get_tk_widget().place(height=350,width=350,x=400,y=10)
	ax=figure.add_subplot(111,projection='3d')
	try:
		a4=float(txt35.get())
		a5=float(txt36.get())
		a6=float(txt37.get())
	except:
		messagebox.showinfo('Error: Not enough data','Please, we need the coordinates of the center of the figure')

	if cmb20.get()=="cone" or cmb20.get()=="cylinder":
		try:
			a1=float(txt31.get())
			a2=float(txt32.get())
		except:
			messagebox.showinfo('Error: Not enough data','Please, we need the value of the radio and the height')
	if cmb20.get()=="sphere":
		try:
			a1=float(txt31.get())
		except:
			messagebox.showinfo('Error: Not enough data','Please, we need the value of the radio')
	if cmb20.get()=="orthohedron":
		try:
			a1=float(txt31.get())
			a2=float(txt32.get())
			a3=float(txt33.get())
		except:
			messagebox.showinfo('Error: Not enough data','Please, we need the value of each side')
	if cmb20.get()=="cone":
		x,y,z=cone(a1,a2)
	if cmb20.get()=="cylinder":
		x,y,z=cylinder(a1,a2)
	if cmb20.get()=="sphere":
		x,y,z=sphere(a1)
	if cmb20.get()=="orthohedron":
		x,y,z=orthohedron(a1,a2,a3)
	x=x+a4
	y=y+a5
	z=z+a6
	ax.set_xticks([np.amin(x),(np.amin(x)+np.amax(x))/2,np.amax(x)])
	ax.set_yticks([np.amin(y),(np.amin(y)+np.amax(y))/2,np.amax(y)])
	ax.set_zticks([np.amin(z),(np.amin(z)+np.amax(z))/2,np.amax(z)])
	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	ax.plot_surface(x, y, z, color='b')

	plt.show()





btn30=tk.Button(aplicacion_3,text="Draw",command=clk30,fg="red")
btn30.place(height=90,width=60,x=310,y=60)

cmb24=ttk.Combobox(aplicacion_3, values=["zxz","xyz","yzx","zyx","zxy","yxz","xzy","zyz","xzx","xyx","yxy","yzy"])
cmb24.place(height=30,width=50,x=275,y=160)
cmb24.current(0)

lbl41=tk.Label(aplicacion_3,text="Rotate figure in Euler's angles[0-360]",anchor=tk.W)
lbl41.place(height=30,width=255,x=10,y=160)

lbl42=tk.Label(aplicacion_3,text="φ:",anchor=tk.W)
lbl42.place(height=30,width=15,x=10,y=190)
lbl43=tk.Label(aplicacion_3,text="θ:",anchor=tk.W)
lbl43.place(height=30,width=15,x=105,y=190)
lbl44=tk.Label(aplicacion_3,text="ψ:",anchor=tk.W)
lbl44.place(height=30,width=15,x=200,y=190)

txt38=tk.Entry(aplicacion_3,text="")
txt38.place(height=30,width=65,x=30,y=190)
txt39=tk.Entry(aplicacion_3,text="")
txt39.place(height=30,width=65,x=125,y=190)
txt40=tk.Entry(aplicacion_3,text="")
txt40.place(height=30,width=65,x=220,y=190)


def clk31():
	global x,y,z,RD,TD,LD
	figure=plt.Figure(figsize=(6,5),dpi=100)
	bar1=FigureCanvasTkAgg(figure,aplicacion_3)
	bar1.get_tk_widget().place(height=350,width=350,x=400,y=10)
	ax=figure.add_subplot(111,projection='3d')

	try:
		a1=float(txt38.get())
		a2=float(txt39.get())
		a3=float(txt40.get())
	except:
		messagebox.showinfo('Error: Not enough data','Please, we need the value of each angle')
	if d==1:
		#ea=np.array([a1,a2,a3])
		#ea=ea*np.pi/180
		#ea=fs.euler2cuat(ea)
		r = R.from_euler(cmb24.get(), [a1, a2 ,a3], degrees=True)
		ea=r.as_quat()
		ea=np.array([ea[3],ea[0],ea[1],ea[2]])
		ea=quat.quaternion(*ea)
		for i,a in enumerate(x):
			for j,b in enumerate(a):
				aux=np.array([0,x[i][j],y[i][j],z[i][j]])
				aux=quat.quaternion(*aux)
				aux=ea*aux*np.conjugate(ea)
				x[i][j]=aux.x
				y[i][j]=aux.y
				z[i][j]=aux.z
		aux=np.array([0,RD[0],RD[1],RD[2]])
		aux=quat.quaternion(*aux)
		aux=ea*aux*np.conjugate(ea)
		RD[0]=aux.x
		RD[1]=aux.y
		RD[2]=aux.z

		aux=np.array([0,LD[0],LD[1],LD[2]])
		aux=quat.quaternion(*aux)
		aux=ea*aux*np.conjugate(ea)
		LD[0]=aux.x
		LD[1]=aux.y
		LD[2]=aux.z

		aux=np.array([0,TD[0],TD[1],TD[2]])
		aux=quat.quaternion(*aux)
		aux=ea*aux*np.conjugate(ea)
		TD[0]=aux.x
		TD[1]=aux.y
		TD[2]=aux.z

	else:
		messagebox.showinfo('Error: Invalid action','Please, you need to draw the figure first')


	ax.set_xticks([np.amin(x),(np.amin(x)+np.amax(x))/2,np.amax(x)])
	ax.set_yticks([np.amin(y),(np.amin(y)+np.amax(y))/2,np.amax(y)])
	ax.set_zticks([np.amin(z),(np.amin(z)+np.amax(z))/2,np.amax(z)])
	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	ax.plot_surface(x, y, z, color='b')
	plt.show()


btn31=tk.Button(aplicacion_3,text="Rotate",command=clk31,fg="red")
btn31.place(height=30,width=60,x=310,y=190)


lbl25=tk.Label(aplicacion_3,text="Move the figure (distance in [cm])",anchor=tk.W)
lbl25.place(height=30,width=300,x=10,y=230)

lbl26=tk.Label(aplicacion_3,text="x:",anchor=tk.W)
lbl26.place(height=30,width=15,x=10,y=270)
lbl27=tk.Label(aplicacion_3,text="y:",anchor=tk.W)
lbl27.place(height=30,width=15,x=105,y=270)
lbl28=tk.Label(aplicacion_3,text="z:",anchor=tk.W)
lbl28.place(height=30,width=15,x=200,y=270)

txt26=tk.Entry(aplicacion_3,text="")
txt26.place(height=30,width=65,x=30,y=270)
txt27=tk.Entry(aplicacion_3,text="")
txt27.place(height=30,width=65,x=130,y=270)
txt28=tk.Entry(aplicacion_3,text="")
txt28.place(height=30,width=65,x=220,y=270)

def clk26():
	global x,y,z
	try:
		a1=float(txt26.get())
		a2=float(txt27.get())
		a3=float(txt28.get())
	except:
		messagebox.showinfo('Error: Not enough data','Please, we need the value of each coordinate')
	if d==1:
		x=x+a1
		y=y+a2
		z=z+a3
	else:
		messagebox.showinfo('Error: Invalid action','Please, you need to draw the figure first')

	figure=plt.Figure(figsize=(6,5),dpi=100)
	bar1=FigureCanvasTkAgg(figure,aplicacion_3)
	bar1.get_tk_widget().place(height=350,width=350,x=400,y=10)
	ax=figure.add_subplot(111,projection='3d')

	ax.set_xticks([np.amin(x),(np.amin(x)+np.amax(x))/2,np.amax(x)])
	ax.set_yticks([np.amin(y),(np.amin(y)+np.amax(y))/2,np.amax(y)])
	ax.set_zticks([np.amin(z),(np.amin(z)+np.amax(z))/2,np.amax(z)])
	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	ax.plot_surface(x, y, z, color='b')
	plt.show()

btn26=tk.Button(aplicacion_3,text="Move",command=clk26,fg="red")
btn26.place(height=30,width=60,x=310,y=270)


lbl45=tk.Label(aplicacion_3,text="Specify the orientation of the: \n(cosine directors)[0-1]",anchor=tk.W)
lbl45.place(height=60,width=200,x=10,y=310)



lbl46=tk.Label(aplicacion_3,text="cos(α):",anchor=tk.W)
lbl46.place(height=30,width=45,x=10,y=370)
lbl47=tk.Label(aplicacion_3,text="cos(β):",anchor=tk.W)
lbl47.place(height=30,width=45,x=100,y=370)
lbl48=tk.Label(aplicacion_3,text="cos(γ):",anchor=tk.W)
lbl48.place(height=30,width=45,x=190,y=370)

var1=tk.StringVar()
var1.set("1")
var2=tk.StringVar()
var2.set("0")
var3=tk.StringVar()
var3.set("0")

txt41=tk.Entry(aplicacion_3,textvariable=var1)
txt41.place(height=30,width=35,x=60,y=370)
txt42=tk.Entry(aplicacion_3,textvariable=var2)
txt42.place(height=30,width=35,x=150,y=370)
txt43=tk.Entry(aplicacion_3,textvariable=var3)
txt43.place(height=30,width=35,x=240,y=370)




def clk_cmb21(event):
	if cmb21.get()=="RD":
		var1.set(RD[0])
		var2.set(RD[1])
		var3.set(RD[2])
	if cmb21.get()=="LD":
		var1.set(LD[0])
		var2.set(LD[1])
		var3.set(LD[2])
	if cmb21.get()=="TD":
		var1.set(TD[0])
		var2.set(TD[1])
		var3.set(TD[2])
	


cmb21=ttk.Combobox(aplicacion_3, values=["RD","LD","TD"])
cmb21.bind("<<ComboboxSelected>>", clk_cmb21)
cmb21.place(height=30,width=50,x=220,y=325)
cmb21.current(0)



def clk32():
	if cmb21.get()=="ND":
		ND[0]=float(txt41.get())
		ND[1]=float(txt42.get())
		ND[2]=float(txt43.get())
	if cmb21.get()=="LD":
		LD[0]=float(txt41.get())
		LD[1]=float(txt42.get())
		LD[2]=float(txt43.get())
	if cmb21.get()=="TD":
		TD[0]=float(txt41.get())
		TD[1]=float(txt42.get())
		TD[2]=float(txt43.get())

btn32=tk.Button(aplicacion_3,text="Fix \n values",command=clk32,fg="red")
btn32.place(height=80,width=60,x=310,y=320)

def clk33():
	np.savez('New_geometry',x=x,y=y,z=z,ND=ND,LD=LD,TD=TD)
	

btn33=tk.Button(aplicacion_3,text="Save geometry",command=clk33,fg="red")
btn33.place(height=30,width=120,x=20,y=410)

def clk34():
	global x,y,z,ND,LD,TD,d
	name=filedialog.askopenfilename(title = "Select file",filetypes = (("geometry files","*.npz"),("all files","*.*")))
	try:
		aux=np.load(name)
		x=aux['x']
		y=aux['y']
		z=aux['z']
		ND=aux['ND']
		LD=aux['LD']
		TD=aux["TD"]
		d=1
		figure=plt.Figure(figsize=(6,5),dpi=100)
		bar1=FigureCanvasTkAgg(figure,aplicacion_3)
		bar1.get_tk_widget().place(height=350,width=350,x=400,y=10)
		ax=figure.add_subplot(111,projection='3d')
		ax.set_xticks([np.amin(x),(np.amin(x)+np.amax(x))/2,np.amax(x)])
		ax.set_yticks([np.amin(y),(np.amin(y)+np.amax(y))/2,np.amax(y)])
		ax.set_zticks([np.amin(z),(np.amin(z)+np.amax(z))/2,np.amax(z)])
		ax.set_xlabel("X")
		ax.set_ylabel("Y")
		ax.set_zlabel("Z")
		ax.plot_surface(x, y, z, color='b')
		plt.show()

	except:
		messagebox.showinfo('Error: Invalid File','Please, we need *txt create by this software without external modification')


btn34=tk.Button(aplicacion_3,text="Load geometry",command=clk34,fg="red")
btn34.place(height=30,width=120,x=160,y=410)


## Beam direction 

figure=plt.Figure(figsize=(6,5),dpi=100)
bar1=FigureCanvasTkAgg(figure,aplicacion_4)
bar1.get_tk_widget().place(height=350,width=350,x=400,y=10)
ax=figure.add_subplot(111,projection='3d')
plt.show()




lbl65=tk.Label(aplicacion_4,text="Define the beam direction by:",anchor=tk.W)
lbl65.place(height=30,width=285,x=10,y=20)

def clk_cmb41(event):
	global lbl66,lbl67,lbl68
	if cmb41.get()=="cosine directors in the laboratory system":
		lbl66=tk.Label(aplicacion_4,text="cos(α):",anchor=tk.W)
		lbl66.place(height=30,width=50,x=10,y=100)
		lbl67=tk.Label(aplicacion_4,text="cos(β):",anchor=tk.W)
		lbl67.place(height=30,width=50,x=110,y=100)
		lbl68=tk.Label(aplicacion_4,text="cos(γ):",anchor=tk.W)
		lbl68.place(height=30,width=50,x=210,y=100)

	if cmb41.get()=="cosine directors in the sample system":
		lbl66=tk.Label(aplicacion_4,text="cos(ND):",anchor=tk.W)
		lbl66.place(height=30,width=50,x=10,y=100)
		lbl67=tk.Label(aplicacion_4,text="cos(TD):",anchor=tk.W)
		lbl67.place(height=30,width=50,x=110,y=100)
		lbl68=tk.Label(aplicacion_4,text="cos(LD):",anchor=tk.W)
		lbl68.place(height=30,width=50,x=210,y=100)


cmb41=ttk.Combobox(aplicacion_4, values=["cosine directors in the laboratory system","cosine directors in the sample system"])
cmb41.bind("<<ComboboxSelected>>", clk_cmb41)
cmb41.place(height=30,width=285,x=10,y=60)
cmb41.current(0)

lbl66=tk.Label(aplicacion_4,text="cos(α):",anchor=tk.W)
lbl66.place(height=30,width=50,x=10,y=100)
lbl67=tk.Label(aplicacion_4,text="cos(β):",anchor=tk.W)
lbl67.place(height=30,width=50,x=110,y=100)
lbl68=tk.Label(aplicacion_4,text="cos(γ):",anchor=tk.W)
lbl68.place(height=30,width=50,x=210,y=100)

txt61=tk.Entry(aplicacion_4,text="")
txt61.place(height=30,width=45,x=60,y=100)
txt62=tk.Entry(aplicacion_4,text="")
txt62.place(height=30,width=45,x=160,y=100)
txt63=tk.Entry(aplicacion_4,text="")
txt63.place(height=30,width=45,x=260,y=100)



def vector_z(ax):
	#Vector en Z
	ax.quiver(0,0,0,2*beam[0],2*beam[1],2*beam[2],color='r')

def clk40():
	global beam
	try:
		a1=float(txt61.get())
		a2=float(txt62.get())
		a3=float(txt63.get())
	except:
		messagebox.showinfo('Error: Not enough data','Please, we need the value of each angle')

	if cmb41.get()=="cosine directors in the laboratory system":
		beam=np.array([a1,a2,a3])
	if cmb41.get()=="cosine directors in the sample system":
		beam=np.array([a1*(ND[0]+TD[0]+LD[0]),a2*(ND[1]+TD[1]+LD[1]),a3*(ND[2]+TD[2]+LD[2])])

	if d==1:
		figure=plt.Figure(figsize=(6,5),dpi=100)
		bar1=FigureCanvasTkAgg(figure,aplicacion_4)
		bar1.get_tk_widget().place(height=350,width=350,x=400,y=10)
		ax=figure.add_subplot(111,projection='3d')
		if ckvar1.get():
				try:
					a4=float(txt67.get())
					a5=float(txt68.get())
					a6=float(txt69.get())
				except:
					messagebox.showinfo('Error: Not enough data','Please, we need the value of each cooNDinates')
		else:
			a4=0
			a5=0
			a6=0
		if a1!=0:
			aux_x=np.linspace(np.amin(x)*1.35,np.amax(x)*1.35,100)
			aux=(aux_x-a4)/a1
			aux_y=a5+aux*a2
			aux_z=a6+aux*a3
		elif a2!=0:
			aux_y=np.linspace(np.amin(y)*1.35,np.amax(y)*1.35,100)
			aux=(aux_y-a5)/a2
			aux_x=a4+aux*a1
			aux_z=a6+aux*a3
		elif a3!=0:
			aux_z=np.linspace(np.amin(z)*1.35,np.amax(z)*1.35,100)
			aux=(aux_y-a6)/a3
			aux_x=a4+aux*a1
			aux_y=a5+aux*a2
		else:
			messagebox.showinfo('Error: Invalid data','The values given for the beam are not valilid')
		

		ax.set_xticks([np.amin(x),(np.amin(x)+np.amax(x))/2,np.amax(x)])
		ax.set_yticks([np.amin(y),(np.amin(y)+np.amax(y))/2,np.amax(y)])
		ax.set_zticks([np.amin(z),(np.amin(z)+np.amax(z))/2,np.amax(z)])
		ax.set_xlabel("X")
		ax.set_ylabel("Y")
		ax.set_zlabel("Z")
		ax.plot_surface(x, y, z, color='b',alpha=0.5)
		ax.plot(aux_x,aux_y,aux_z,color='r',linewidth=8)
		plt.show()

btn40=tk.Button(aplicacion_4,text="Set",command=clk40,fg="red")
btn40.place(height=60,width=60,x=310,y=90)

lbl75=tk.Label(aplicacion_4,text="x:",anchor=tk.W)
lbl75.place(height=30,width=15,x=10,y=180)
lbl76=tk.Label(aplicacion_4,text="y:",anchor=tk.W)
lbl76.place(height=30,width=15,x=95,y=180)
lbl77=tk.Label(aplicacion_4,text="z:",anchor=tk.W)
lbl77.place(height=30,width=15,x=180,y=180)

txt67=tk.Entry(aplicacion_4,text="0",state=tk.DISABLED)
txt67.place(height=30,width=55,x=30,y=180)
txt68=tk.Entry(aplicacion_4,text="0",state=tk.DISABLED)
txt68.place(height=30,width=55,x=115,y=180)
txt69=tk.Entry(aplicacion_4,text="0",state=tk.DISABLED)
txt69.place(height=30,width=55,x=200,y=180)

ckvar1=tk.BooleanVar()
def clk_ckb1():
	global ckvar1,txt67,txt68,txt69
	if ckvar1.get():
		txt67=tk.Entry(aplicacion_4,text="",state=tk.NORMAL)
		txt67.place(height=30,width=55,x=30,y=180)
		txt68=tk.Entry(aplicacion_4,text="",state=tk.NORMAL)
		txt68.place(height=30,width=55,x=115,y=180)
		txt69=tk.Entry(aplicacion_4,text="",state=tk.NORMAL)
		txt69.place(height=30,width=55,x=200,y=180)
	else:
		txt67=tk.Entry(aplicacion_4,text="",state=tk.DISABLED)
		txt67.place(height=30,width=55,x=30,y=180)
		txt68=tk.Entry(aplicacion_4,text="",state=tk.DISABLED)
		txt68.place(height=30,width=55,x=115,y=180)
		txt69=tk.Entry(aplicacion_4,text="",state=tk.DISABLED)
		txt69.place(height=30,width=55,x=200,y=180)


ckb1=ttk.Checkbutton(aplicacion_4,text="Define beam impact coordinates",command=clk_ckb1,variable=ckvar1)
ckb1.place(height=30,width=285,x=10,y=150)
ckvar1.set(False)

lbl69=tk.Label(aplicacion_4,text="Define rotation in the beam direction by:",anchor=tk.W)
lbl69.place(height=30,width=285,x=10,y=230)


lbl70=tk.Label(aplicacion_4,text="φ:",anchor=tk.W)
lbl70.place(height=30,width=25,x=10,y=300)
lbl71=tk.Label(aplicacion_4,text="θ:",anchor=tk.W)
lbl71.place(height=30,width=25,x=100,y=300)
lbl72=tk.Label(aplicacion_4,text="ψ:",anchor=tk.W)
lbl72.place(height=30,width=25,x=190,y=300)

txt64=tk.Entry(aplicacion_4,text="")
txt64.place(height=30,width=55,x=35,y=300)
txt65=tk.Entry(aplicacion_4,text="")
txt65.place(height=30,width=55,x=130,y=300)
txt66=tk.Entry(aplicacion_4,text="")
txt66.place(height=30,width=55,x=220,y=300)

def clk_cmb42(event):
	global lbl70,lbl71,lbl72,txt66
	if cmb42.get()=="euler angles in the laboratory system" or cmb42.get()=="euler angles in the sample system":
		txt66.place(height=30,width=55,x=220,y=300)
		lbl70=tk.Label(aplicacion_4,text="φ:",anchor=tk.W)
		lbl70.place(height=30,width=25,x=10,y=300)
		lbl71=tk.Label(aplicacion_4,text="θ:",anchor=tk.W)
		lbl71.place(height=30,width=25,x=100,y=300)
		lbl72=tk.Label(aplicacion_4,text="ψ:",anchor=tk.W)
		lbl72.place(height=30,width=25,x=190,y=300)
	if cmb42.get()=="α and β in the sample system":
		txt66.place(height=0,width=0,x=0,y=0)
		lbl70=tk.Label(aplicacion_4,text="α:",anchor=tk.W)
		lbl70.place(height=30,width=25,x=10,y=300)
		lbl71=tk.Label(aplicacion_4,text="β:",anchor=tk.W)
		lbl71.place(height=30,width=25,x=100,y=300)
		lbl72=tk.Label(aplicacion_4,text="    ",anchor=tk.W)
		lbl72.place(height=30,width=25,x=190,y=300)


cmb42=ttk.Combobox(aplicacion_4, values=["euler angles in the laboratory system","euler angles in the sample system","α and β in the sample system"])
cmb42.bind("<<ComboboxSelected>>", clk_cmb42)
cmb42.place(height=30,width=285,x=10,y=260)
cmb42.current(0)


def clk41():
	global direcciones,list_dirc
	if cmb42.get()!="α and β in the sample system":
		try:
			a1=float(txt64.get())
			a2=float(txt65.get())
			a3=float(txt66.get())
		except:
			messagebox.showinfo('Error: Not enough data','Please, we need the value of each angle')
		i=str(len(direcciones.keys()))
		direcciones[i]={'#':int(i),'φ':a1,'θ':a2,'ψ':a3,'α':None,'β':None}
		list_dirc.insert("","end",iid=int(i),values=(i,a1,a2,a3,None,None))
	else:
		try:
			a1=float(txt64.get())
			a2=float(txt65.get())
		except:
			messagebox.showinfo('Error: Not enough data','Please, we need the value of each angle')
		i=str(len(direcciones.keys()))
		direcciones[i]={'#':int(i),'φ':None,'θ':None,'ψ':None,'α':a1,'β':a2}
		list_dirc.insert("","end",iid=int(i),values=(i,None,None,None,a1,a2))




btn41=tk.Button(aplicacion_4,text="Save \n Rotation",command=clk41,fg="red")
btn41.place(height=60,width=80,x=310,y=270)

#Create a Treeview to show the rotation

cols=('#','φ','θ','ψ','α','β')
list_dirc=ttk.Treeview(aplicacion_4,columns=cols,show='headings')
list_dirc.place(height=150,width=300,x=10,y=350)
list_dirc.column('#',width=40,minwidth=30)
list_dirc.column('φ',width=40,minwidth=30)
list_dirc.column('θ',width=40,minwidth=30)
list_dirc.column('ψ',width=40,minwidth=30)
list_dirc.column('α',width=40,minwidth=30)
list_dirc.column('β',width=40,minwidth=30)
for col in cols:
	list_dirc.heading(col,text=col)


lbl78=tk.Label(aplicacion_4,text="Eliminate rotation in position:",anchor=tk.W)
lbl78.place(height=30,width=220,x=350,y=370)

txt75=tk.Entry(aplicacion_4,text="")
txt75.place(height=30,width=35,x=560,y=370)

def clk42():
	global direcciones,list_dirc

	try:
		a1=int(txt75.get())
	except:
		messagebox.showinfo('Error: Invalid data','Invalid number of rotation')
	if int(len(direcciones.keys()))<a1:
		messagebox.showinfo('Error: Invalid data','The rotation doesnt exist')
		return 0
	list_dirc.delete(a1)
	direcciones.pop(str(a1))
	aux=list_dirc.get_children()
	for item in aux:
		if int(item)>a1:
			list_dirc.insert("","end",iid=(int(item)-1),values=(str(int(list_dirc.item(item,option="values")[0])-1),list_dirc.item(item,option="values")[1],list_dirc.item(item,option="values")[2],list_dirc.item(item,option="values")[3],list_dirc.item(item,option="values")[4],list_dirc.item(item,option="values")[5]))
			list_dirc.delete(item)
			direcciones[str(int(item)-1)]=direcciones.pop(item)
			direcciones[str(int(item)-1)]['#']=direcciones[str(int(item)-1)]['#']-1


btn42=tk.Button(aplicacion_4,text="Eliminate",command=clk42,fg="red")
btn42.place(height=30,width=80,x=620,y=370)

lbl80=tk.Label(aplicacion_4,text="Save the list of rotation",anchor=tk.W)
lbl80.place(height=30,width=500,x=350,y=420)

lbl79=tk.Label(aplicacion_4,text="Click            to use the \"WizaND-import\" to  load a list of rotation",anchor=tk.W)
lbl79.place(height=30,width=500,x=350,y=460)

def clk43():
	salida=open("rotaciones.txt",'w')
	salida.write("φ\tθ\tψ\tα\tβ\n")
	for ii in direcciones.keys():
		aux=str(direcciones[ii]['φ'])+"\t"+str(direcciones[ii]['θ'])+"\t"+str(direcciones[ii]['ψ'])+"\t" +str(direcciones[ii]['α'])+"\t"+str(direcciones[ii]['β'])+"\n"
		salida.write(aux)

btn43=tk.Button(aplicacion_4,text="Save",command=clk43,fg="red")
btn43.place(height=30,width=60,x=480,y=420)

def clk44():
	global direcciones,list_dirc
	file = filedialog.askopenfilename(filetypes = (("Data files","*.dat"),("Matlab files","*.mat"),("Text files","*.txt"),("all files","*.*")))
	wiz.import_list(file)
	rotaciones=wiz.datos_finales
	for i in range (rotaciones.shape[1]):
		direcciones[i]={'#':int(i),'φ':rotaciones[0][i],'θ':rotaciones[1][i],'ψ':rotaciones[2][i],'α':rotaciones[3][i],'β':rotaciones[4][i]}
		list_dirc.insert("","end",iid=int(i),values=(i,rotaciones[0][i],rotaciones[1][i],rotaciones[2][i],rotaciones[3][i],rotaciones[4][i]))

btn44=tk.Button(aplicacion_4,text="Here",command=clk44,fg="red")
btn44.place(height=30,width=40,x=390,y=460)

# More of the simulation step

def run():
	global neutron_path,radius
	if len(direcciones.keys())==0:
		messagebox.showinfo('Error: One step incomplete','No rotations loaded')
		return 0
	try:
		modos[0]
	except:
		messagebox.showinfo('Error: One step incomplete','No texture loaded')
		return 0

	for ii in range (int(var_aux_1.get()),int(var_aux_2.get())):
		
		alpha=direcciones[str(ii)]['α']*np.pi/180
		
		beta=direcciones[str(ii)]['β']*np.pi/180
		#Beam_rot=np.array([np.sin(alpha),np.cos(alpha)*np.cos(beta),-np.cos(alpha)*np.sin(beta)])
		
		Beam_rot=np.cos(alpha)*ND+np.sin(alpha)*np.sin(beta)*LD-np.sin(alpha)*np.cos(beta)*TD

		#lbl_run=tk.Label(aplicacion_5,text="The rotation "+str(ii)+" is running",anchor=tk.W)
		#lbl_run.place(height=30,width=320,x=10,y=650)

		p=np.zeros(2000)
		p_aux_2=np.zeros((modos.shape[1],2000))
		lam=np.linspace(1.5,6.0,2000)
		
		if radVar4.get()==1:
			
			for i in range (modos.shape[1]):
				print(i)
				
				# The progress bar doesnt work, dont konw why
				#bar = ttk.Progressbar(aplicacion_5, length=100)
				#bar.place(height=30,width=400,x=10,y=300)
				#if i%(modos.shape[1]//10)==0:
				#	bar['value']=int(i*100/modos.shape[1])
				if modos.shape[0]==5:
					r = R.from_quat([modos[1][i], modos[2][i], modos[3][i], modos[4][i]])
				if modos.shape[0]==4:
					r= R.from_euler('zxz',[modos[1][i],modos[2][i],modos[3][i]],degrees=True)
				if modos.shape[0]==6:
					r= R.from_euler('zxz',[modos[1][i],modos[2][i],modos[3][i]],degrees=True)	
					radius=modos[5][i]	
				r=r.inv()
				
				aux=r.apply(Beam_rot)
				

				p_aux_2[i]=fs.Simular_dir_angles(aux,lam,radVar2.get(),radius)
				p+=modos[0][i]*p_aux_2[i]

			salida=open("out/datos"+str(ii)+".txt",'w')
			for i,j in enumerate (p):
				salida.write(str(lam[i])+"\t"+str(j)+"\n")
			salida=open("out/modes"+str(ii)+".txt",'w')
			for i in range (2000):
				salida.write(str(lam[i]))
				for j in range (modos.shape[1]):
					salida.write("\t"+str(p_aux_2[j][i]))
				salida.write("\n")

			
		else:
			#radVar4.get()
			p_aux=np.zeros(2000)
			for a in range (4,180,4):
				for b in range (4,180,4):
					for c in range (4,180,4):
						r = R.from_euler("zxz", [a,b,c], degrees=True)
						r=r.inv()
						aux=r.apply(Beam_rot)
						p_aux+=1/79507*fs.Simular_dir_angles(aux,lam,radVar2.get())
			p=(1-float(var_aux_weigth.get()))*p_aux
			for i in range (0,int(var_aux_modes)):
				r = R.from_quat([modos[1][i], modos[2][i], modos[3][i], modos[4][i]])
				r=r.inv()
				aux=r.apply(Beam_rot)			
				p+=modos[0][i]*fs.Simular_dir_angles(aux,lam,radVar2.get())

			salida=open("out/datos"+str(ii)+"mod"+str(var_aux_modes)+".txt",'w')
			for i,j in enumerate (p):
				salida.write(str(lam[i])+"\t"+str(j/0.0844/2)+"\n")


		
		if ckvar2.get() and ckvar3.get():
			if radVar3.get()==1:
				aux=0
				lam_lim=10
				#Only use next line if want skip the main function
				#lam,p=np.loadtxt("out/datos"+str(ii)+".txt",delimiter="\t",usecols =(0, 1),unpack = True)
				#lambd=transmision[ii]['lambda']
				while len(lambd)==1:
					lambd=lambd[0]
				tr=transmision[ii]['trans']
				while len(tr)==1:
					tr=tr[0]
				
				for pos,j in enumerate (p):
					if j<0.001 and aux==0:
						lam_lim=lam[pos]
						aux=1

				count=0
				dist=0
				sec_no=fs.interpolacion(sec_no_elas_coh,lambd)

				for pos,j in enumerate (lambd[:-10]):
					if j>lam_lim and count <200:
						count+=1
						dist+=-np.log(float(tr[pos]))/(sec_no[pos]*0.0844)
				dist=dist/count
				print(dist)
				
				cross_section=np.zeros(tr.shape[0])
				for pos,j in enumerate(lambd):
					cross_section[pos]=-np.log(tr[pos])/(dist*0.0844)

				salida_2=open("out/cross_s"+str(ii)+".txt",'w')
				for i,j in enumerate (cross_section):
					salida_2.write(str(lambd[i])+"\t"+str(j)+"\n")	
				
			if radVar3.get()==2:
				
				
				#Other method to be sure
				r = R.from_euler("zxz", [0,beta*180/3.1415,(alpha)*180/3.1415], degrees=True)
				r=R.inv(r)

				min_x=0
				max_x=0
				dist_min=100
				dist_max=100
				for i,a in enumerate(x):
					for j,b in enumerate(a):
						aux=np.array([x[i][j],y[i][j],z[i][j]])
												
						aux=r.apply(aux)
						if aux[2]**2+aux[1]**2<dist_min and aux[0]<0:
							dist_min=aux[2]**2+aux[1]**2
							min_x=aux[0]
						if aux[2]**2+aux[1]**2<dist_max and aux[0]>0:
							dist_max=aux[2]**2+aux[1]**2
							max_x=aux[0]
									
				print(max_x-min_x)

			if radVar1.get()==3:
				#Verify that path is not empty
				asf=1		
	

btn_run=tk.Button(aplicacion_5, text="Run", command=run,anchor=tk.W,highlightcolor="red")
btn_run.place(height=50, width=80,y=340,x=650)

ckvar2=tk.BooleanVar()

radVar3=tk.IntVar() #Beam path in the sample

ckvar3=tk.BooleanVar() #Include non Bragg componet of cross section

def clks2():
	asf=1
	#Load neutron path from a file

def clks3():
	global transmision
	name=filedialog.askopenfilename(title = "Select file",filetypes = (("MatLab files","*.mat"),("data files","*.dat"),("text files","*.txt"),("all files","*.*")))
	wiz_trans.import_list(name)
	transmision=wiz_trans.datos_finales

def clk_rad2():
	if radVar3.get()==3:
		btns2=tk.Button(aplicacion_5, text="Load", command=clks2,anchor=tk.W,state=tk.NORMAL)
		btns2.place(height=30, width=80,y=260,x=200)
		btns3=tk.Button(aplicacion_5, text="Load data", command=clks3,anchor=tk.W,state=tk.DISABLED)
		btns3.place(height=30, width=100,y=200,x=200)
	if radVar3.get()==1:
		btns3=tk.Button(aplicacion_5, text="Load data", command=clks3,anchor=tk.W,state=tk.NORMAL)
		btns3.place(height=30, width=100,y=200,x=200)
		btns2=tk.Button(aplicacion_5, text="Load", command=clks2,anchor=tk.W,state=tk.DISABLED)
		btns2.place(height=30, width=80,y=260,x=200)
	if radVar3.get()==2:
		btns3=tk.Button(aplicacion_5, text="Load data", command=clks3,anchor=tk.W,state=tk.DISABLED)
		btns3.place(height=30, width=100,y=200,x=200)
		btns2=tk.Button(aplicacion_5, text="Load", command=clks2,anchor=tk.W,state=tk.DISABLED)
		btns2.place(height=30, width=80,y=260,x=200)		

rads4=tk.Radiobutton(aplicacion_5,text="Experimental data",variable=radVar3,value=1,command=clk_rad2,anchor=tk.W,state=tk.DISABLED)
rads4.place(height=30,width=150,x=30,y=200)

rads5=tk.Radiobutton(aplicacion_5,text="Geometry",variable=radVar3,value=2,command=clk_rad2,anchor=tk.W,state=tk.DISABLED)
rads5.place(height=30,width=150,x=30,y=230)

rads6=tk.Radiobutton(aplicacion_5,text="External file",variable=radVar3,value=3,command=clk_rad2,anchor=tk.W,state=tk.DISABLED)
rads6.place(height=30,width=150,x=30,y=260)

radVar3.set(1)
btns2=tk.Button(aplicacion_5, text="Load", command=clks2,anchor=tk.W,state=tk.DISABLED)
btns2.place(height=30, width=80,y=260,x=200)

btns3=tk.Button(aplicacion_5, text="Load data", command=clks3,anchor=tk.W,state=tk.DISABLED)
btns3.place(height=30, width=100,y=200,x=200)

def clk_ckb2():
	if ckvar2.get():
		rads4=tk.Radiobutton(aplicacion_5,text="Experimental data",variable=radVar3,value=1,command=clk_rad2,anchor=tk.W,state=tk.NORMAL)
		rads4.place(height=30,width=150,x=30,y=200)

		rads5=tk.Radiobutton(aplicacion_5,text="Geometry",variable=radVar3,value=2,command=clk_rad2,anchor=tk.W,state=tk.NORMAL)
		rads5.place(height=30,width=150,x=30,y=230)

		rads6=tk.Radiobutton(aplicacion_5,text="External file",variable=radVar3,value=3,command=clk_rad2,anchor=tk.W,state=tk.NORMAL)
		rads6.place(height=30,width=150,x=30,y=260)
		clk_rad2()
	else:
		rads4=tk.Radiobutton(aplicacion_5,text="Experimental data",variable=radVar3,value=1,command=clk_rad2,anchor=tk.W,state=tk.DISABLED)
		rads4.place(height=30,width=150,x=30,y=200)

		rads5=tk.Radiobutton(aplicacion_5,text="Geometry",variable=radVar3,value=2,command=clk_rad2,anchor=tk.W,state=tk.DISABLED)
		rads5.place(height=30,width=150,x=30,y=230)

		rads6=tk.Radiobutton(aplicacion_5,text="External file",variable=radVar3,value=3,command=clk_rad2,anchor=tk.W,state=tk.DISABLED)
		rads6.place(height=30,width=150,x=30,y=260)
		btns2=tk.Button(aplicacion_5, text="Load", command=clks2,anchor=tk.W,state=tk.DISABLED)
		btns2.place(height=30, width=80,y=260,x=200)


ckb2=ttk.Checkbutton(aplicacion_5,text="Calculate transmision using neutron path \n inside the sample define by:",command=clk_ckb2,variable=ckvar2)
ckb2.place(height=50,width=350,x=10,y=150)
ckvar2.set(False)

def clk_ckb3():
	if ckvar3.get():
		btns4=tk.Button(aplicacion_5, text="Load", command=clks4,anchor=tk.W,state=tk.NORMAL)
		btns4.place(height=30, width=80,y=300,x=350)
	else:
		btns4=tk.Button(aplicacion_5, text="Load", command=clks4,anchor=tk.W,state=tk.DISABLED)
		btns4.place(height=30, width=80,y=300,x=350)

ckb2=ttk.Checkbutton(aplicacion_5,text="Include non-Bragg component of cross section",command=clk_ckb3,variable=ckvar3)
ckb2.place(height=30,width=320,x=10,y=300)
ckvar3.set(False)

def clks4():
	global sec_no_elas_coh
	name=filedialog.askopenfilename(title = "Select file",filetypes = (("text files","*.txt"),("MatLab files","*.mat"),("data files","*.dat"),("all files","*.*")))
	wiz_sec.import_list(name)
	sec_no_elas_coh=wiz_sec.datos_finales

btns4=tk.Button(aplicacion_5, text="Load", command=clks4,anchor=tk.W,state=tk.DISABLED)
btns4.place(height=30, width=80,y=300,x=350)

aplicacion_3.tkraise()


figure=plt.Figure(figsize=(6,5),dpi=100)
bar1=FigureCanvasTkAgg(figure,aplicacion_3)
bar1.get_tk_widget().place(height=350,width=350,x=400,y=10)
ax=figure.add_subplot(111,projection='3d')


## Aplicacion_6 Adjust function to transmission


def aplicacion_6_raise():
	if len (direcciones.keys())==0:
		lbl6_1=tk.Label(aplicacion_6,text="Directions need to be loaded (Go to BEAM section, to do it )",fg="red",anchor=tk.W)
		lbl6_1.place(height=30,width=450,x=10,y=10)
	else:
		lbl6_1=tk.Label(aplicacion_6,text=str(len(direcciones.keys()))+" rotation directions have been loaded",anchor=tk.W)
		lbl6_1.place(height=30,width=450,x=10,y=10)
	if estructura==0:
		lbl6_2=tk.Label(aplicacion_6,text="Structure need to be loaded (Go to SIMULATION section, to do it )",fg="red",anchor=tk.W)
		lbl6_2.place(height=30,width=450,x=10,y=40)
	else:
		lbl6_2=tk.Label(aplicacion_6,text="Structure loaded successfully",anchor=tk.W)
		lbl6_2.place(height=30,width=450,x=10,y=40)	
	if len (transmision.keys())==0:
		lbl6_3=tk.Label(aplicacion_6,text="Experimental data need to be loaded",fg="red",anchor=tk.W)
		lbl6_3.place(height=30,width=300,x=10,y=70)
		btn6_1=tk.Button(aplicacion_6, text="Load", command=clk6_1,anchor=tk.W,state=tk.NORMAL)
		btn6_1.place(height=30, width=80,y=70,x=310)
	else:
		lbl6_3=tk.Label(aplicacion_6,text="Experimental data loaded successfully",anchor=tk.W)
		lbl6_3.place(height=30,width=300,x=10,y=70)
		btn6_1=tk.Button(aplicacion_6, text="Load", command=clk6_1,anchor=tk.W,state=tk.DISABLED)
		btn6_1.place(height=30, width=80,y=70,x=310)

	lbl6_4=tk.Label(aplicacion_6,text="Base of functions are needed",fg="red",anchor=tk.W)
	lbl6_4.place(height=30,width=300,x=10,y=110)
	btn6_2=tk.Button(aplicacion_6, text="Generate", command=clk6_2,anchor=tk.W,state=tk.NORMAL)
	btn6_2.place(height=30, width=80,y=110,x=310)	
	btn6_3=tk.Button(aplicacion_6, text="Load", command=clk6_3,anchor=tk.W,state=tk.NORMAL)
	btn6_3.place(height=30, width=80,y=110,x=410)		

def clk6_1():
	global datos_ajuste
	aux=filedialog.askopenfilenames(title="Select files", filetypes=(("text files","*.txt"),("data files","*.dat"),("all files","*.*")))
	aux=list(aux)
	aux_2=np.loadtxt(aux[0],delimiter='\t')
	datos_ajuste=np.zeros((len(aux),len(aux_2)))
	for i,elemt in enumerate(aux):
		aux_2=np.loadtxt(elemt,delimiter='\t')
		for j in range (len(aux_2)):
			datos_ajuste[i][j]=aux_2[j] #Need to change this, to a import wizard

		


def clk6_2():

	for ii in range (len(direcciones.keys())):
		
		alpha=direcciones[ii]['α']
		beta=direcciones[ii]['β']

		Beam_rot=np.cos(alpha)*ND+np.sin(alpha)*np.cos(beta)*LD+np.sin(alpha)*np.sin(beta)*TD

		lam=np.array(transmision[ii]['lambda'][0])
		p=np.zeros(lam.shape[0])

		base_function=np.zeros((modos.shape[1],lam.shape[0]))

		for i in range (modos.shape[1]):
				
			r = R.from_quat([modos[1][i], modos[2][i], modos[3][i], modos[4][i]])
			r=r.inv()
			aux=r.apply(Beam_rot)			
			p_aux=fs.Simular_dir_angles(aux,lam,radVar2.get())
			for j in range (lam.shape[0]):
				base_function[i][j]=p_aux[j]/0.0844/2
			p+=p_aux*modos[0][i]

		np.savetxt("Adjust/Base/Base"+str(ii)+".csv",base_function,delimiter=',')
		#data=np.loadtxt("Adjust/Base/Base"+str(ii)+".csv",delimiter=',')

		salida=open("Adjust/Experimental/datos"+str(ii)+".txt",'w')
		for i,j in enumerate (p):
			salida.write(str(lam[i])+"\t"+str(j/0.0844/2)+"\n")
def clk6_3():
	global function_base
	aux=filedialog.askopenfilenames(title="Select files", filetypes=(("Function base","*.csv"),("data files","*.dat"),("all files","*.*")))
	aux=list(aux)
	for i,elemt in enumerate(aux):
		print(i)
		function_base[str(i)]=np.loadtxt(elemt,delimiter=',')



def funct_ajuste(params,exp, data=[]):
	aux=np.zeros((len(exp.keys()),exp['1'].shape[1]))
	for i,ii in enumerate(exp.keys()):
		datos=exp[ii]	
		for j in range (datos.shape[0]):
			aux[i]+=params["C"+str(j)].value*datos[j]
	if data==[]:
		return aux
	return data-aux

ckvar_ajuste=tk.BooleanVar()
ckvar_no_elast=tk.BooleanVar()

def ajuste_run():

	if ckvar_no_elast.get():
		for i in range (datos_ajuste.shape[0]):
			for j in range(datos_ajuste.shape[1]):
				datos_ajuste[i][j]=datos_ajuste[i][j]-sec_no_elas[j]
	modes=int(modes_adjust.get())
	print(modes,len(modes_init))
	fit_params=lm.Parameters()
	if ckvar_modes_init.get():
		for j in range(len(modes_init)):
			fit_params.add("C"+str(j),value=float(modes_init[j]),min=0,max=0.1)
		for j in range (len(modes_init),modes):
			fit_params.add("C"+str(j),value=0.001,min=0,max=0.1)
	else:
		for j in range (modes):
			fit_params.add("C"+str(j),value=0.01,min=0,max=0.1)
	fit_params.add("C"+str(modes),value=0.5,min=0,max=1)
	function_base_parcial={}
	for i,ii in enumerate(function_base.keys()):
		datos=function_base[ii]
		aux=np.zeros((modes+1,datos.shape[1]))
		for j in range (modes):
			for k in range(datos.shape[1]):
				aux[j][k]=datos[j][k]
		if ckvar_ajuste.get():
			for k in range (datos.shape[1]):
				aux[modes][k]=sec_powder[k]
		else:			
			for j in range (modes,datos.shape[0]):
				for k in range (datos.shape[1]):
					aux[modes][k]+=datos[j][k]*modos[0][j]
		function_base_parcial[ii]=aux

	print("Termino esa fase")
	out=lm.minimize(funct_ajuste,fit_params,args=(function_base_parcial,datos_ajuste))
	print(lm.fit_report(out))
	for name,param in out.params.items():
		print(param.value)

btn6_run=tk.Button(aplicacion_6, text="Run", command=ajuste_run,anchor=tk.W,state=tk.NORMAL)
btn6_run.place(height=30, width=80,y=350,x=410)	

def clk6_4():	
	lam=np.array(transmision[1]['lambda'][0])	
	p=np.zeros(lam.shape[0])
	for a in range (10,180,10):
		print(a)
		for b in range (10,180,10):
			for c in range (10,180,10):
				r = R.from_euler("zxz", [a,b,c], degrees=True)
				r=r.inv()
				aux=r.apply(np.array([1,0,0]))
				p+=1/4096*fs.Simular_dir_angles(aux,lam,radVar2.get())
	p=p/0.0844/2
	np.savetxt("Adjust/Base/powder.csv",p,delimiter=',')
	for ii in lam:
		print(ii)
	


def clk6_5():
	global sec_powder
	aux=filedialog.askopenfilename(title="Select files", filetypes=(("Function base","*.csv"),("data files","*.dat"),("all files","*.*")))
	sec_powder=np.loadtxt(aux,delimiter=',')

def clk_ckb6_1():
	if ckvar_ajuste.get():
		btn6_4=tk.Button(aplicacion_6, text="Generate", command=clk6_4,anchor=tk.W,state=tk.NORMAL)
		btn6_4.place(height=30, width=80,y=150,x=230)	
		btn6_5=tk.Button(aplicacion_6, text="Load", command=clk6_5,anchor=tk.W,state=tk.NORMAL)
		btn6_5.place(height=30, width=80,y=150,x=320)
	else:
		btn6_4=tk.Button(aplicacion_6, text="Generate", command=clk6_4,anchor=tk.W,state=tk.DISABLED)
		btn6_4.place(height=30, width=80,y=150,x=230)	
		btn6_5=tk.Button(aplicacion_6, text="Load", command=clk6_5,anchor=tk.W,state=tk.DISABLED)
		btn6_5.place(height=30, width=80,y=150,x=320)		

ckb6_1=ttk.Checkbutton(aplicacion_6,text="Use powder cross section",command=clk_ckb6_1,variable=ckvar_ajuste)
ckb6_1.place(height=30,width=200,x=10,y=150)
ckvar_ajuste.set(False)

def clk6_7():
	global sec_no_elas
	aux=filedialog.askopenfilename(title="Select files", filetypes=(("Function base","*.csv"),("data files","*.dat"),("all files","*.*")))
	sec_no_elas=np.loadtxt(aux,delimiter=',')

def clk_ckb6_3():
	if ckvar_no_elast.get():
		btn6_7=tk.Button(aplicacion_6, text="Load", command=clk6_7,anchor=tk.W,state=tk.NORMAL)
		btn6_7.place(height=30, width=80,y=240,x=320)
	else:
		btn6_7=tk.Button(aplicacion_6, text="Load", command=clk6_7,anchor=tk.W,state=tk.DISABLED)
		btn6_7.place(height=30, width=80,y=240,x=320)		

ckb6_3=ttk.Checkbutton(aplicacion_6,text="Subtract the cross section not-elastic coherent",command=clk_ckb6_3,variable=ckvar_no_elast)
ckb6_3.place(height=30,width=300,x=10,y=240)
ckvar_no_elast.set(False)

lbl6_5=tk.Label(aplicacion_6,text="Select number of modes to adjust:",fg="red",anchor=tk.W)
lbl6_5.place(height=30,width=300,x=10,y=180)

modes_adjust=tk.StringVar()
spn6_1 = tk.Spinbox(aplicacion_6, from_=0, to=10000,textvariable=modes_adjust,state=tk.NORMAL)
spn6_1.place(height=30,width=70,x=310,y=180)
modes_adjust.set("50")
ckvar_modes_init=tk.BooleanVar()
modes_init=[]
def clk6_6():
	global modes_init
	aux=filedialog.askopenfilename(title="Select files", filetypes=(("text files","*.txt"),("data files","*.dat"),("all files","*.*")))
	file=open(aux,"r")
	for ii in file:
		modes_init.append(ii)
def clk_ckb6_1():
	if ckvar_modes_init.get():
		btn6_6=tk.Button(aplicacion_6, text="Load", command=clk6_6,anchor=tk.W,state=tk.NORMAL)
		btn6_6.place(height=30, width=80,y=210,x=320)
	else:
		btn6_6=tk.Button(aplicacion_6, text="Load", command=clk6_6,anchor=tk.W,state=tk.DISABLED)
		btn6_6.place(height=30, width=80,y=210,x=320)		

ckb6_2=ttk.Checkbutton(aplicacion_6,text="Use previous result to initialize the adjust",command=clk_ckb6_1,variable=ckvar_modes_init)
ckb6_2.place(height=30,width=300,x=10,y=210)
ckvar_modes_init.set(False)

window.mainloop()


