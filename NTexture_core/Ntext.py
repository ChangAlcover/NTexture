import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import PIL

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.spatial.transform import Rotation as R
import subprocess
import project_class as cl
import Functions as fun

# Global variables for class
project = cl.Project()
lststp=cl.Last_step()
material = cl.Material()
simulation=cl.Simulation("1")
geometry = cl.Geometry("1")
ODF= cl.ODF()

## Main window 
window = tk.Tk()
window.geometry('600x600')
window.resizable(0, 0)
window.title("NTexture")

##Any number of sub windows in the same position to every step

Welcome = tk.LabelFrame(window)
Welcome.place(height=600, width=600, x=0, y=0)
Welcome.tkraise()

New_exp = tk.LabelFrame(window,text="New experiment")
New_exp.place(height=600, width=600, x=0, y=0)

step_mat = tk.LabelFrame(window, text="Material selection")
step_mat.place(height=600, width=600, x=0, y=0)

new_mat = tk.LabelFrame(window, text="Material creation")
new_mat.place(height=600, width=600, x=0, y=0)

geometry_option = tk.LabelFrame(window, text="Geometry option")
geometry_option.place(height=600, width=600, x=0, y=0)

geometry_definition = tk.LabelFrame(window, text="Geometry definition")
geometry_definition.place(height=600, width=600, x=0, y=0)

odf_v = tk.LabelFrame(window, text="ODF")
odf_v.place(height=600, width=600, x=0, y=0)

inst_v = tk.LabelFrame(window, text="Instrument information")
inst_v.place(height=350, width=600, x=0, y=250)

exp_v = tk.LabelFrame(window, text="Experiment information")
exp_v.place(height=600, width=600, x=0, y=0)

exp_t = tk.LabelFrame(window, text="Experiment information")
exp_t.place(height=600, width=600, x=0, y=0)

exp_s = tk.LabelFrame(window, text="Experiment information")
exp_s.place(height=600, width=600, x=0, y=0)

exp_i = tk.LabelFrame(window, text="Experiment information")
exp_i.place(height=600, width=600, x=0, y=0)

final_v = tk.LabelFrame(window, text="Final step")
final_v.place(height=600, width=600, x=0, y=0)

final_t = tk.LabelFrame(window, text="Final step")
final_t.place(height=600, width=600, x=0, y=0)

final_s = tk.LabelFrame(window, text="Final step")
final_s.place(height=600, width=600, x=0, y=0)

final_i = tk.LabelFrame(window, text="Final step")
final_i.place(height=600, width=600, x=0, y=0)

## Button to go back in every step
def BACK():
	lststp.name.tkraise()

BACK_New_exp = tk.Button(New_exp, text="BACK", command=BACK)
BACK_New_exp.place(height=25, width=50, x=490, y=-5)

BACK_step_mat = tk.Button(step_mat, text="BACK", command=BACK)
BACK_step_mat.place(height=25, width=50, x=490, y=-5)

BACK_new_mat = tk.Button(new_mat, text="BACK", command=BACK)
BACK_new_mat.place(height=25, width=50, x=490, y=-5)

BACK_odf_v = tk.Button(odf_v, text="BACK", command=BACK)
BACK_odf_v.place(height=25, width=50, x=490, y=-5)

BACK_exp_v = tk.Button(exp_v, text="BACK", command=BACK)
BACK_exp_v.place(height=25, width=50, x=490, y=-5)

BACK_exp_t = tk.Button(exp_v, text="BACK", command=BACK)
BACK_exp_t.place(height=25, width=50, x=490, y=-5)

BACK_exp_t = tk.Button(exp_v, text="BACK", command=BACK)
BACK_exp_t.place(height=25, width=50, x=490, y=-5)

BACK_exp_i = tk.Button(exp_v, text="BACK", command=BACK)
BACK_exp_i.place(height=25, width=50, x=490, y=-5)

BACK_final_v = tk.Button(final_v, text="BACK", command=BACK)
BACK_final_v.place(height=25, width=50, x=490, y=-5)

BACK_final_v = tk.Button(final_v, text="BACK", command=BACK)
BACK_final_v.place(height=25, width=50, x=490, y=-5)

BACK_final_v = tk.Button(final_v, text="BACK", command=BACK)
BACK_final_v.place(height=25, width=50, x=490, y=-5)

BACK_final_v = tk.Button(final_v, text="BACK", command=BACK)
BACK_final_v.place(height=25, width=50, x=490, y=-5)



## Subwindow of Welcome

lbl_welcome1 = tk.Label(Welcome, text="NTexture", fg="red", font=("Arial", 40))
lbl_welcome1.place(height=50, width=340, x=130, y=50)
txt_welcome2 = tk.StringVar()
txt_welcome2.set("a software for the simulation of neutron\n transmission experiments")
lbl_welcome2 = tk.Label(Welcome, textvariable=txt_welcome2)
lbl_welcome2.place(height=50, width=340, x=130, y=120)


def click_load_project():
	global project
	file = filedialog.askopenfilename(title="Select name", filetypes=(("Project files", "*.pkl"), ("all files", "*.*")))
	project=project.load_project(file)
	FS.tkraise()
	FS_tree1_update()
	lststp.update(Welcome)


def click_new_project():
    lststp.update(Welcome)
    New_exp.tkraise()


btn_load_project = tk.Button(Welcome, text="Load \n Project", command=click_load_project)
btn_load_project.place(height=50, width=100, x=150, y=230)

btn_new_project = tk.Button(Welcome, text="New \n Project", command=click_new_project)
btn_new_project.place(height=50, width=100, x=350, y=230)

ima_logo=tk.PhotoImage(file='logo.png')
ima_logo=ima_logo.subsample(3,3)
lbl_welcome3 = tk.Label(Welcome, image=ima_logo)
lbl_welcome3.place(height=150, width=550, x=25, y=380)

Welcome.tkraise()


###Select the experiment

New_exp_lbl1 = tk.Label(New_exp, text="Select the experiment and ODF type",font=("Arial", 20))
New_exp_lbl1.place(height=50, width=500, x=50, y=50)

def New_exp_cmb1_click(event):
	global New_exp_lbl2
	if New_exp_cmb1.get()=="Sample rotations":
		New_exp_lbl2 = tk.Label(New_exp, text="Spectra for wavelength range,\n with the neutron beam in different directions \n over the sample\n Geometry: optional")
		New_exp_lbl2.place(height=100, width=400, x=100, y=220)
	elif New_exp_cmb1.get()=="Samples with spatial resolution":
		New_exp_lbl2 = tk.Label(New_exp, text="Spectra for wavelength range,\n in different sections or point of the sample\n Geometry: mandatory")
		New_exp_lbl2.place(height=100, width=400, x=100, y=220)
	elif New_exp_cmb1.get()=="Temperature variations":
		New_exp_lbl2 = tk.Label(New_exp, text="Spectra for wavelength range,\n for different sample temperatures\n Geometry: optional")
		New_exp_lbl2.place(height=100, width=400, x=100, y=220)
	elif New_exp_cmb1.get()=="Transmission images":	
		New_exp_lbl2 = tk.Label(New_exp, text="Sample transmission images for a single\n wavelength or multiple images for different \n rotations or wavelengths\n Geometry: Mandatory")
		New_exp_lbl2.place(height=100, width=400, x=100, y=220)

New_exp_cmb1 = ttk.Combobox(New_exp, values=["Sample rotations","Samples with spatial resolution","Temperature variations","Transmission images"])
New_exp_cmb1.place(height=25, width=350, x=100, y=150)
New_exp_cmb1.bind("<<ComboboxSelected>>", New_exp_cmb1_click)
New_exp_cmb1.set("Sample rotations")

New_exp_lbl2 = tk.Label(New_exp, text="Spectra for wavelength range,\n with the neutron beam in different directions \n over the sample\n Geometry: optional")
New_exp_lbl2.place(height=100, width=400, x=100, y=220)


def New_exp_cmb2_click(event):
	global New_exp_lbl3
	if New_exp_cmb2.get()=="Powder":
		New_exp_lbl3 = tk.Label(New_exp, text="Material with isotropic\n crystallographic distribution")
		New_exp_lbl3.place(height=100, width=400, x=100, y=420)
	elif New_exp_cmb2.get()=="Textured material":
		New_exp_lbl3 = tk.Label(New_exp, text="The Orientation Distribution Function (ODF)\n needs to be supplied in future steps")
		New_exp_lbl3.place(height=100, width=400, x=100, y=420)
	elif New_exp_cmb2.get()=="Monocrystal":
		New_exp_lbl3 = tk.Label(New_exp, text="Sample composed of a single crystal\n with a certain mosaicity")
		New_exp_lbl3.place(height=100, width=400, x=100, y=420)

New_exp_cmb2 = ttk.Combobox(New_exp, values=["Powder","Textured material","Monocrystal"])
New_exp_cmb2.place(height=25, width=350, x=100, y=350)
New_exp_cmb2.bind("<<ComboboxSelected>>", New_exp_cmb2_click)
New_exp_cmb2.set("Powder")


New_exp_lbl3 = tk.Label(New_exp, text="Material with isotropic\n crystallographic distribution")
New_exp_lbl3.place(height=100, width=400, x=100, y=420)

def New_exp_btn1_click():
	global project
	lststp.update(New_exp)
	project = cl.Project(New_exp_cmb1.get())
	step_mat.tkraise()


New_exp_btn1 = tk.Button(New_exp, text="Next", command=New_exp_btn1_click)
New_exp_btn1.place(height=45, width=80, x=490, y=520)

##Subwindow Step1: Select the material
# Users can choose one for our database or create/modify a new one

step_mat_lbl1 = tk.Label(step_mat,font=("Arial", 16),text="Options for selecting materials:")
step_mat_lbl1.place(height=70, width=400, x=100, y=25)

step_mat_lbl2 = tk.Label(step_mat,text="Load a material from NTexture database \n (located in DATA folder)")
step_mat_lbl2.place(height=100, width=300, x=50, y=125)

step_mat_lbl3 = tk.Label(step_mat,text="Create a new material \n It's necessary to know the crystal structure")
step_mat_lbl3.place(height=100, width=300, x=50, y=250)

step_mat_lbl4 = tk.Label(step_mat,text="Modify and use a material from the database \n The density can be modified or \n the values of cross section can be supplied")
step_mat_lbl4.place(height=100, width=300, x=50, y=370)



def click_load_material():
	global material
	file = filedialog.askopenfilename(title="Select name", filetypes=(("Data files", "*.pkl"), ("all files", "*.*")))
	material=material.load_material(file)
	lststp.update(step_mat)
	geometry_option.tkraise()


def click_new_material():
    new_mat.tkraise()
    lststp.update(step_mat)
    new_mat.tkraise()

def click_modify_material():
	a=1	


btn_load_material = tk.Button(step_mat, text="Load \n material", command=click_load_material)
btn_load_material.place(height=50, width=100, x=400, y=150)

btn_new_material = tk.Button(step_mat, text="New \n material", command=click_new_material)
btn_new_material.place(height=50, width=100, x=400, y=275)

btn_modify_material = tk.Button(step_mat, text="Modify \n material", command=click_modify_material)
btn_modify_material.place(height=50, width=100, x=400, y=400)


## Subwindow to create a new material
# First the lattice parameters

new_mat_lbl1 = tk.Label(new_mat, text="Lattice parameters:")
new_mat_lbl1.place(height=30, width=200, x=25, y=3)

new_mat_lbl2 = tk.Label(new_mat, text="a:\t    b: \t       c:\t \nα:\t    β: \t       γ:\t ", font=("Arial", 14),anchor=tk.W)
new_mat_lbl2.place(height=60, width=300, x=75, y=30)

new_mat_lbl2_1 = tk.Label(new_mat,text="[Å]  \n[degree]", font=("Arial", 12),anchor=tk.W)
new_mat_lbl2_1.place(height=60, width=70, x=375, y=30)

new_mat_txt1 = tk.Entry(new_mat, text="")
new_mat_txt1.place(height=20, width=70, x=100, y=40)
new_mat_txt2 = tk.Entry(new_mat, text="")
new_mat_txt2.place(height=20, width=70, x=195, y=40)
new_mat_txt3 = tk.Entry(new_mat, text="")
new_mat_txt3.place(height=20, width=70, x=290, y=40)
new_mat_txt4 = tk.Entry(new_mat, text="")
new_mat_txt4.place(height=20, width=70, x=100, y=60)
new_mat_txt5 = tk.Entry(new_mat, text="")
new_mat_txt5.place(height=20, width=70, x=195, y=60)
new_mat_txt6 = tk.Entry(new_mat, text="")
new_mat_txt6.place(height=20, width=70, x=290, y=60)

new_mat_lbl1_1 = tk.Label(new_mat, text="Material data:",font=("Arial", 12),anchor=tk.W)
new_mat_lbl1_1.place(height=30, width=200, x=25, y=100)

new_mat_lbl3_1 = tk.Label(new_mat, text="Load information for the atom:",font=("Arial", 12),anchor=tk.W)
new_mat_lbl3_1.place(height=30, width=220, x=35, y=150)


def new_mat_cmb1_click(event):
	global new_mat_nc
	if new_mat_cmb1.get()=="Be":
		new_mat_M.set("9.0122")
		new_mat_n.set("2")
		new_mat_b.set("7.79")
		new_mat_u.set("0.0066")	
		new_mat_nc.set("NCrystal/Instalacion/data/Be_sg194.ncmat")	
		new_mat_name.set("Be")
	elif new_mat_cmb1.get()=="C_Pyrolytic":
		new_mat_M.set("12.011")
		new_mat_n.set("6")
		new_mat_b.set("6.6484")
		new_mat_u.set("1.00181")	
		new_mat_nc.set("NCrystal/Instalacion/data/C_sg194_pyrolytic_graphite.ncmat")
		new_mat_name.set("C_Pyrolytic")
	elif new_mat_cmb1.get()=="C_Diamond":
		new_mat_M.set("12.011")
		new_mat_n.set("8")
		new_mat_b.set("6.6484")
		new_mat_u.set("0.00181")	
		new_mat_nc.set("NCrystal/Instalacion/data/C_sg227_Diamond.ncmat")
		new_mat_name.set("C_Diamond")
	elif new_mat_cmb1.get()=="Bi":
		new_mat_M.set("208.98")
		new_mat_n.set("6")
		new_mat_b.set("8.532")
		new_mat_u.set("0.02677")	
		new_mat_nc.set("NCrystal/Instalacion/data/Bi.ncmat")
		new_mat_name.set("Bi")
	elif new_mat_cmb1.get()=="Mg":
		new_mat_M.set("24.305")
		new_mat_n.set("6")
		new_mat_b.set("5.376")
		new_mat_u.set("0.02303")	
		new_mat_nc.set("NCrystal/Instalacion/data/Mg_sg194.ncmat")
		new_mat_name.set("Mg")
	elif new_mat_cmb1.get()=="Al":
		new_mat_M.set("26.982")
		new_mat_n.set("4")
		new_mat_b.set("3.449")
		new_mat_u.set("0.0102")	
		new_mat_nc.set("NCrystal/Instalacion/data/Al_sg225.ncmat")
		new_mat_name.set("Al")
	elif new_mat_cmb1.get()=="Ti":
		new_mat_M.set("47.88")
		new_mat_n.set("6")
		new_mat_b.set("-3.37")
		new_mat_u.set("0.0066")	
		new_mat_nc.set("NCrystal/Instalacion/data/Ti_sg194.ncmat")	
		new_mat_name.set("Ti")
	elif new_mat_cmb1.get()=="Fe_alpha":
		new_mat_M.set("55.847")
		new_mat_n.set("2")
		new_mat_b.set("9.45")
		new_mat_u.set("0.00426")	
		new_mat_nc.set("NCrystal/Instalacion/data/Fe_sg229_Iron-alpha.ncmat")
		new_mat_name.set("Fe_alpha")
	elif new_mat_cmb1.get()=="Ni":
		new_mat_M.set("55.69")
		new_mat_n.set("4")
		new_mat_b.set("10.3")
		new_mat_u.set("0.00463")	
		new_mat_nc.set("NCrystal/Instalacion/data/Ni_sg225.ncmat")
		new_mat_name.set("Ni")
	elif new_mat_cmb1.get()=="Cu":
		new_mat_M.set("63.546")
		new_mat_n.set("4")
		new_mat_b.set("7.718")
		new_mat_u.set("0.00704")	
		new_mat_nc.set("NCrystal/Instalacion/data/Cu_sg225.ncmat")
		new_mat_name.set("Cu")
	elif new_mat_cmb1.get()=="Zr":
		new_mat_M.set("91.224")
		new_mat_n.set("6")
		new_mat_b.set("7.16")
		new_mat_u.set("0.00722")	
		new_mat_nc.set("NCrystal/Instalacion/data/Zr_sg194.ncmat")
		new_mat_name.set("Zr")
	elif new_mat_cmb1.get()=="Nb":
		new_mat_M.set("92.906")
		new_mat_n.set("2")
		new_mat_b.set("7.054")
		new_mat_u.set("0.00571")	
		new_mat_nc.set("NCrystal/Instalacion/data/Nb_sg229.ncmat")
		new_mat_name.set("Nb")
	elif new_mat_cmb1.get()=="Pb":
		new_mat_M.set("207.2")
		new_mat_n.set("4")
		new_mat_b.set("9.401")
		new_mat_u.set("0.02677")	
		new_mat_nc.set("NCrystal/Instalacion/data/Pb_sg225.ncmat")
		new_mat_name.set("Pb")
	elif new_mat_cmb1.get()=="Mo":
		new_mat_M.set("95.94")
		new_mat_n.set("2")
		new_mat_b.set("6.715")
		new_mat_u.set("0.00279")	
		new_mat_nc.set("NCrystal/Instalacion/data/Mo_sg229.ncmat")
		new_mat_name.set("Mo")
	elif new_mat_cmb1.get()=="Sn":
		new_mat_M.set("118.71")
		new_mat_n.set("4")
		new_mat_b.set("6.225")
		new_mat_u.set("0.01436")	
		new_mat_nc.set("NCrystal/Instalacion/data/Sn_sg141.ncmat")
		new_mat_name.set("Sn")
	elif new_mat_cmb1.get()=="Si":
		new_mat_M.set("28.086")
		new_mat_n.set("8")
		new_mat_b.set("4.15")
		new_mat_u.set("0.00653")	
		new_mat_nc.set("NCrystal/Instalacion/data/Si_sg227.ncmat")
		new_mat_name.set("Si")
	elif new_mat_cmb1.get()=="Na":
		new_mat_M.set("22.99")
		new_mat_n.set("2")
		new_mat_b.set("3.63")
		new_mat_u.set("0.0837")	
		new_mat_nc.set("NCrystal/Instalacion/data/Na_sg229.ncmat")
		new_mat_name.set("Na")
	elif new_mat_cmb1.get()=="V":
		new_mat_M.set("50.942")
		new_mat_n.set("2")
		new_mat_b.set("-0.443")
		new_mat_u.set("0.0067")	
		new_mat_nc.set("NCrystal/Instalacion/data/V_sg229.ncmat")
		new_mat_name.set("V")
	elif new_mat_cmb1.get()=="Cr":
		new_mat_M.set("51.996")
		new_mat_n.set("2")
		new_mat_b.set("3.635")
		new_mat_u.set("0.0033")	
		new_mat_nc.set("NCrystal/Instalacion/data/Cr_sg229.ncmat")
		new_mat_name.set("Cr")
	elif new_mat_cmb1.get()=="Zn":
		new_mat_M.set("65.39")
		new_mat_n.set("6")
		new_mat_b.set("5.68")
		new_mat_u.set("0.0144")	
		new_mat_nc.set("NCrystal/Instalacion/data/Zn_sg194.ncmat")
		new_mat_name.set("Zn")
	elif new_mat_cmb1.get()=="Ge":
		new_mat_M.set("72.59")
		new_mat_n.set("8")
		new_mat_b.set("8.185")
		new_mat_u.set("0.00077")	
		new_mat_nc.set("NCrystal/Instalacion/data/Ge_sg227.ncmat")
		new_mat_name.set("Ge")
	elif new_mat_cmb1.get()=="Y":
		new_mat_M.set("88.9")
		new_mat_n.set("6")
		new_mat_b.set("7.75")
		new_mat_u.set("0.0107")	
		new_mat_nc.set("NCrystal/Instalacion/data/Y_sg194.ncmat")
		new_mat_name.set("Y")
	elif new_mat_cmb1.get()=="Pd":
		new_mat_M.set("106342")
		new_mat_n.set("4")
		new_mat_b.set("5.91")
		new_mat_u.set("0.00567")	
		new_mat_nc.set("NCrystal/Instalacion/data/Pd_sg225.ncmat")
		new_mat_name.set("Pd")
	elif new_mat_cmb1.get()=="Ag":
		new_mat_M.set("107.87")
		new_mat_n.set("4")
		new_mat_b.set("5.922")
		new_mat_u.set("0.00926")	
		new_mat_nc.set("NCrystal/Instalacion/data/Ag_sg225.ncmat")
		new_mat_name.set("Ag")
	elif new_mat_cmb1.get()=="W":
		new_mat_M.set("183.85")
		new_mat_n.set("2")
		new_mat_b.set("4.755")
		new_mat_u.set("0.00203")	
		new_mat_nc.set("NCrystal/Instalacion/data/W_sg229.ncmat")
		new_mat_name.set("W")	


new_mat_cmb1 = ttk.Combobox(new_mat, values=["Be", "C_Pyrolytic","C_Diamond","Bi","Mg","Al","Ti","Fe_alpha","Ni","Cu","Zr","Nb","Pb","Mo","Sn","Si","Na","V","Cr","Zn","Ge","Y","Pd","Ag","W"])
new_mat_cmb1.place(height=25, width=110, x=265, y=150)
new_mat_cmb1.bind("<<ComboboxSelected>>", new_mat_cmb1_click)

new_mat_lbl1_2 = tk.Label(new_mat, text="Density[g/cm3]:\t\t  or    M[g/mol]:\n     N. of atoms in unit cell:",anchor=tk.W)
new_mat_lbl1_2.place(height=50, width=350, x=75, y=190)

new_mat_M=tk.StringVar()
new_mat_n=tk.StringVar()
new_mat_b=tk.StringVar()
new_mat_u=tk.StringVar()
new_mat_nc=tk.StringVar()
new_mat_name=tk.StringVar()

new_mat_txt1_1 = tk.Entry(new_mat, text="")
new_mat_txt1_1.place(height=20, width=70, x=183, y=197)
new_mat_txt2_1 = tk.Entry(new_mat, text=new_mat_M)
new_mat_txt2_1.place(height=20, width=70, x=370, y=197)
new_mat_txt3_1 = tk.Entry(new_mat, text=new_mat_n)
new_mat_txt3_1.place(height=20, width=50, x=312, y=215)


# Also the Wyckoff position are nedeed

new_mat_lbl3 = tk.Label(new_mat,
                        text="Wyckoff position, scatering length and \n mean square displacement of the atom: ",font=("Arial", 12),anchor=tk.W)
new_mat_lbl3.place(height=40, width=400, x=25, y=250)


new_mat_lbl4 = tk.Label(new_mat, text="x:\t y:\t z:\t\n b:    \t   <u²>: \t\t", font=("Arial", 14))
new_mat_lbl4.place(height=60, width=250, x=55, y=300)

new_mat_txt7 = tk.Entry(new_mat, text="")
new_mat_txt7.place(height=20, width=60, x=75, y=310)
new_mat_txt8 = tk.Entry(new_mat, text="")
new_mat_txt8.place(height=20, width=60, x=160, y=310)
new_mat_txt9 = tk.Entry(new_mat, text="")
new_mat_txt9.place(height=20, width=60, x=240, y=310)
new_mat_txt10 = tk.Entry(new_mat, text=new_mat_b)
new_mat_txt10.place(height=20, width=60, x=80, y=332)
new_mat_txt11 = tk.Entry(new_mat, text=new_mat_u)
new_mat_txt11.place(height=20, width=60, x=200, y=332)

cols_tree_new_mat = ('x', 'y', 'z', 'b', '<u²>')
tree_new_mat = ttk.Treeview(new_mat, columns=cols_tree_new_mat, show='headings')
tree_new_mat.place(height=130, width=300, x=30, y=380)
tree_new_mat.column('x', width=50, minwidth=30)
tree_new_mat.column('y', width=50, minwidth=30)
tree_new_mat.column('z', width=50, minwidth=30)
tree_new_mat.column('b', width=75, minwidth=30)
tree_new_mat.column('<u²>', width=75, minwidth=30)
for col in cols_tree_new_mat:
    tree_new_mat.heading(col, text=col)


def click_add_attom():
    global tree_new_mat
    try:
        tree_new_mat.insert("", tk.END, values=(
        float(new_mat_txt7.get()), float(new_mat_txt8.get()), float(new_mat_txt9.get()), float(new_mat_txt10.get()),
        float(new_mat_txt11.get())))
    except:
        tk.messagebox.showinfo('Error: Invalid data type',
                               "Please, make sure a numeric value was entered for each parameter")


btn2_new_mat = tk.Button(new_mat, text="Add \n atom", command=click_add_attom)
btn2_new_mat.place(height=60, width=50, x=370, y=300)


def click_attom_finish():
	global material
	material = cl.Material()
	try:
		material.add_lattice(float(new_mat_txt1.get()), float(new_mat_txt2.get()), float(new_mat_txt3.get()),
                             float(new_mat_txt4.get()), float(new_mat_txt5.get()), float(new_mat_txt6.get()))
	except:
		tk.messagebox.showinfo('Error: Invalid data type',
                               "Please, make sure a numeric value was entered for each lattice parameter")
	try:
		material.add_data(new_mat_txt1_1.get(), new_mat_txt2_1.get(), new_mat_txt3_1.get())
	except:
		tk.messagebox.showinfo('Error: Invalid data type',
                               "Please, make sure a numeric value was entered for each parameter")
	material.add_estruct(tree_new_mat)
	if len(material.struct) == 0 or material.a == material.b == material.c == 0:
		tk.messagebox.showinfo('Error: No Wyckoff position loaded',
                               "Please, load the Wyckoff position to define a new material")
	else:
		if new_mat_txt12.get()=="":
			aux="new_material"
		else:
			aux=new_mat_txt12.get()
		file = "Data_base/" + aux + ".pkl"
		material.add_name(aux)
		material.add_dir(new_mat_nc.get())
		material.save_material(file)
		lststp.update(new_mat)
		geometry_option.tkraise()


btn3_new_mat = tk.Button(new_mat, text="Finish",  command=click_attom_finish, font=("Arial", 14))
btn3_new_mat.place(height=60, width=60, x=480, y=500)


new_mat_lbl5 = tk.Label(new_mat, text="Material name:", anchor=tk.W)
new_mat_lbl5.place(height=30, width=200, x=5, y=530)
new_mat_txt12 = tk.Entry(new_mat, text=new_mat_name)
new_mat_txt12.place(height=30, width=190, x=115, y=530)

## Step 2: Geometry option
# Users can skip this step and give the neutron path lenght in the sample

geometry_option_lbl = tk.Label(geometry_option,
                               text="Create or load a geometry,\n Can skip if geometry was optional \n on the experiment choosen",font=("Arial", 14))
geometry_option_lbl.place(height=150, width=315, x=145, y=25)


def click_create_geometry():
    geometry_definition.tkraise()
    lststp.update(geometry_option)


def click_skip_geometry():
    global geometry
    geometry = cl.Geometry("1")
    if New_exp_cmb1.get()=="Samples with spatial resolution"or New_exp_cmb1.get()=="Transmission images":
    	tk.messagebox.showinfo('Geometry required',
                               "Please, geometry information is needed")
    else:
    	lststp.update(geometry_option)
    	odf_option()

def click_load_geometry():
    global geometry
    file = filedialog.askopenfilename(title="Select name", filetypes=(("Data files", "*.pkl"), ("all files", "*.*")))
    geometry=geometry.load(file)
    lststp.update(geometry_option)
    odf_option()



btn_create_geometry = tk.Button(geometry_option, text="Define \n geometry", command=click_create_geometry)
btn_create_geometry.place(height=50, width=100, x=145, y=200)

btn_skip_mgeometry = tk.Button(geometry_option, text="Skip \n geometry", command=click_skip_geometry)
btn_skip_mgeometry.place(height=50, width=100, x=325, y=200)

btn_load_mgeometry = tk.Button(geometry_option, text="Load \n geometry", command=click_load_geometry)
btn_load_mgeometry.place(height=50, width=100, x=243, y=300)

geometry_option_lbl2 = tk.Label(geometry_option,text="Geometry is optional in experiments:\n Sample rotations \n Temperature variations")
geometry_option_lbl2.place(height=150, width=315, x=145, y=400)

### Geometry definition (simplification GD)

figure = plt.Figure(figsize=(9, 7.5), dpi=100)
bar1 = FigureCanvasTkAgg(figure, geometry_definition)
bar1.get_tk_widget().place(height=250, width=250, x=10, y=300)
Fig_GD = figure.add_subplot(111, projection='3d')

GD_lbl1 = tk.Label(geometry_definition, text="a:", anchor=tk.W)
GD_lbl2 = tk.Label(geometry_definition, text="b:", anchor=tk.W)
GD_lbl3 = tk.Label(geometry_definition, text="c:", anchor=tk.W)
GD_lbl4 = tk.Label(geometry_definition, text="r:", anchor=tk.W)
GD_lbl5 = tk.Label(geometry_definition, text="h:", anchor=tk.W)

GD_txt1 = tk.Entry(geometry_definition, text="")
GD_txt2 = tk.Entry(geometry_definition, text="")
GD_txt3 = tk.Entry(geometry_definition, text="")

# By default orthohedron

GD_lbl1.place(height=30, width=15, x=10, y=45)
GD_lbl2.place(height=30, width=15, x=105, y=45)
GD_lbl3.place(height=30, width=15, x=200, y=45)
GD_txt1.place(height=20, width=65, x=30, y=50)
GD_txt2.place(height=20, width=65, x=130, y=50)
GD_txt3.place(height=20, width=65, x=220, y=50)


def click_GD_cmb1(event):
    global GD_lbl1, GD_lbl2, GD_lbl3, GD_lbl4, GD_lbl5, GD_txt1, GD_txt2, GD_txt3

    GD_lbl1.place(height=0, width=0, x=0, y=0)
    GD_lbl2.place(height=0, width=0, x=0, y=0)
    GD_lbl3.place(height=0, width=0, x=0, y=0)
    GD_lbl4.place(height=0, width=0, x=0, y=0)
    GD_lbl5.place(height=0, width=0, x=0, y=0)
    GD_txt1.place(height=0, width=0, x=0, y=0)
    GD_txt2.place(height=0, width=0, x=0, y=0)
    GD_txt3.place(height=0, width=0, x=0, y=0)

    if GD_cmb1.get() == "cylinder":
        GD_lbl4.place(height=30, width=15, x=10, y=45)
        GD_lbl5.place(height=30, width=15, x=105, y=45)
        GD_txt1.place(height=20, width=65, x=30, y=50)
        GD_txt2.place(height=20, width=65, x=130, y=50)
    if GD_cmb1.get() == "sphere":
        GD_lbl4.place(height=30, width=15, x=10, y=45)
        GD_txt1.place(height=20, width=65, x=30, y=50)
    if GD_cmb1.get() == "orthohedron":
        GD_lbl1.place(height=30, width=15, x=10, y=45)
        GD_lbl2.place(height=30, width=15, x=105, y=45)
        GD_lbl3.place(height=30, width=15, x=200, y=45)
        GD_txt1.place(height=20, width=65, x=30, y=50)
        GD_txt2.place(height=20, width=65, x=130, y=50)
        GD_txt3.place(height=20, width=65, x=220, y=50)


GD_cmb1 = ttk.Combobox(geometry_definition, values=["cylinder", "sphere", "orthohedron"])
GD_cmb1.bind("<<ComboboxSelected>>", click_GD_cmb1)
GD_cmb1.place(height=30, width=200, x=20, y=10)
GD_cmb1.current(2)


def click_btn1_GD():
    global geometry
    #try:
    if GD_cmb1.get() == "cylinder":
        if float(GD_txt1.get()) > 0 and float(GD_txt2.get()) > 0:
            geometry = cl.Geometry("2", [GD_txt1.get(), GD_txt2.get()])
            Fig_GD.cla()
            geometry.draw(Fig_GD)
            figure.canvas.draw()
        else:
            tk.messagebox.showinfo('Error: Invalid data type',
                                   "Please, make sure a VALID numeric value was entered for each parameter")
    if GD_cmb1.get() == "sphere":
        if float(GD_txt1.get()) > 0:
            geometry = cl.Geometry("3", [GD_txt1.get()])
            Fig_GD.cla()
            geometry.draw(Fig_GD)
            figure.canvas.draw()
        else:
            tk.messagebox.showinfo('Error: Invalid data type',
                                   "Please, make sure a VALID numeric value was entered for each parameter")
    if GD_cmb1.get() == "orthohedron":
        if float(GD_txt1.get()) > 0 and float(GD_txt2.get()) > 0 and float(GD_txt3.get()) > 0:
            geometry = cl.Geometry("5", [GD_txt1.get(), GD_txt2.get(), GD_txt3.get()])
            Fig_GD.cla()
            geometry.draw(Fig_GD)
            figure.canvas.draw()
        else:
            tk.messagebox.showinfo('Error: Invalid data type',
                                   "Please, make sure a VALID numeric value was entered for each parameter")

   # except:
  #      tk.messagebox.showinfo('Error: Invalid data type',
    #                           "Please, make sure a numeric value was entered for each parameter")


btn1_GD = tk.Button(geometry_definition, text="Create", command=click_btn1_GD)
btn1_GD.place(height=30, width=50, x=350, y=30)

GD_lbl6 = tk.Label(geometry_definition, text="Traslational movements", anchor=tk.W)
GD_lbl6.place(height=30, width=200, x=10, y=75)

GD_lbl7 = tk.Label(geometry_definition, text="x:", anchor=tk.W)
GD_lbl8 = tk.Label(geometry_definition, text="y:", anchor=tk.W)
GD_lbl9 = tk.Label(geometry_definition, text="z:", anchor=tk.W)
GD_txt4 = tk.Entry(geometry_definition, text="")
GD_txt5 = tk.Entry(geometry_definition, text="")
GD_txt6 = tk.Entry(geometry_definition, text="")
GD_txt4.insert(tk.END, "0")
GD_txt5.insert(tk.END, "0")
GD_txt6.insert(tk.END, "0")

GD_lbl7.place(height=30, width=15, x=10, y=100)
GD_lbl8.place(height=30, width=15, x=105, y=100)
GD_lbl9.place(height=30, width=15, x=200, y=100)
GD_txt4.place(height=20, width=65, x=30, y=105)
GD_txt5.place(height=20, width=65, x=130, y=105)
GD_txt6.place(height=20, width=65, x=220, y=105)


def click_btn2_GD():
    if geometry.type == "1":
        tk.messagebox.showinfo('Error: Invalid geometry', "Please, first you need to create the geometry")
    else:
        try:
            geometry.move([float(GD_txt4.get()), float(GD_txt5.get()), float(GD_txt6.get())])
            Fig_GD.cla()
            geometry.draw(Fig_GD)
            figure.canvas.draw()
        except:
            tk.messagebox.showinfo('Error: Invalid data type',
                                   "Please, make sure a numeric value was entered for each parameter")


btn2_GD = tk.Button(geometry_definition, text="Move", command=click_btn2_GD)
btn2_GD.place(height=30, width=50, x=350, y=95)

GD_lbl11 = tk.Label(geometry_definition, text="Rotate figure in Euler's angles[0-360]", anchor=tk.W)
GD_lbl11.place(height=30, width=300, x=10, y=130)

GD_cmb2 = ttk.Combobox(geometry_definition,
                       values=["zxz", "xyz", "yzx", "zyx", "zxy", "yxz", "xzy", "zyz", "xzx", "xyx", "yxy", "yzy"])
GD_cmb2.place(height=30, width=50, x=262, y=130)
GD_cmb2.current(0)

GD_lbl12 = tk.Label(geometry_definition, text="φ:", anchor=tk.W)
GD_lbl13 = tk.Label(geometry_definition, text="θ:", anchor=tk.W)
GD_lbl14 = tk.Label(geometry_definition, text="ψ:", anchor=tk.W)
GD_txt7 = tk.Entry(geometry_definition, text="")
GD_txt8 = tk.Entry(geometry_definition, text="")
GD_txt9 = tk.Entry(geometry_definition, text="")
GD_txt7.insert(tk.END, "0")
GD_txt8.insert(tk.END, "0")
GD_txt9.insert(tk.END, "0")

GD_lbl12.place(height=30, width=15, x=10, y=158)
GD_lbl13.place(height=30, width=15, x=105, y=158)
GD_lbl14.place(height=30, width=15, x=200, y=158)
GD_txt7.place(height=20, width=65, x=30, y=163)
GD_txt8.place(height=20, width=65, x=130, y=163)
GD_txt9.place(height=20, width=65, x=220, y=163)


def click_btn3_GD():
    if geometry.type == "1":
        tk.messagebox.showinfo('Error: Invalid geometry', "Please, first you need to create the geometry")
    else:
        try:
            geometry.add_rotation([GD_cmb2.get(), float(GD_txt7.get()), float(GD_txt8.get()), float(GD_txt9.get())])
            Fig_GD.cla()
            geometry.draw(Fig_GD)
            figure.canvas.draw()
        except:
            tk.messagebox.showinfo('Error: Invalid data type',
                                   "Please, make sure a numeric value was entered for each parameter")


btn3_GD = tk.Button(geometry_definition, text="Rotate", command=click_btn3_GD)
btn3_GD.place(height=30, width=70, x=350, y=140)

GD_lbl15 = tk.Label(geometry_definition, text="Save by the name:", anchor=tk.W)
GD_lbl15.place(height=30, width=150, x=320, y=330)

GD_txt10 = tk.Entry(geometry_definition, text="")
GD_txt10.place(height=30, width=150, x=320, y=370)

def click_btn4_GD():
    if geometry.type == "1":
        tk.messagebox.showinfo('Error: Invalid geometry', "Please, first you need to create the geometry")
    else:
        file = "Geometry/" + GD_txt10.get() + ".pkl"
        geometry.save(file)
        simulation.add_beam(GD_cmb3.get())
        odf_option()
        lststp.update(geometry_definition)


btn4_GD = tk.Button(geometry_definition, text="Save", command=click_btn4_GD)
btn4_GD.place(height=40, width=70, x=360, y=420)

GD_lbl1_1 = tk.Label(geometry_definition, text="Neutron beam direction:", anchor=tk.W)
GD_lbl1_1.place(height=30, width=160, x=15, y=250)

GD_cmb3=ttk.Combobox(geometry_definition, values=["Z axis","Y axis","X axis"])
GD_cmb3.place(height=25,width=70,x=195,y=250)
GD_cmb3.current(0)

def odf_option():
	#New_exp_cmb2 = ttk.Combobox(New_exp, values=["Powder","Textured material","Monocrystal"])
	if New_exp_cmb2.get()=="Textured material":
		odf_v_lbl1=tk.Label(odf_v,text="The option \"Texture material\" was selected,\n therefore a function of distribution of orientatios(ODF) is necessary:\n 1- If it was previosly created,\n it can be loaded from the ODF database\n 2-A new one can be created from a list\n of modes or Fourier coefficients")
		odf_v_lbl1.place(height=100,width=500,x=50,y=25)
		def load_ODF_click():
			file = filedialog.askopenfilename(title="Select name", filetypes=(("Data files", "*.pkl"), ("all files", "*.*")))
			ODF.load(file)
			inst_inf()

		def create_ODF_click():
			wizard_modes()

		btn_load_ODF = tk.Button(odf_v, text="Load ODF\n(databse)", command=load_ODF_click)
		btn_load_ODF.place(height=50, width=120, x=130, y=170)

		btn_create_ODF = tk.Button(odf_v, text="Create \n ODF", command=create_ODF_click)
		btn_create_ODF.place(height=50, width=120, x=350, y=170)
		odf_v.tkraise()

	if New_exp_cmb2.get()=="Monocrystal":
		odf_v_lbl1=tk.Label(odf_v,text="The option \"Monocrystal\" was selected,\n therefore necessary to define the direction:\n of the single crystal in the laboratory,\n reference system and its mosaicity")
		odf_v_lbl1.place(height=80,width=500,x=50,y=25)
		
		odf_v_lbl2=tk.Label(odf_v,text="Direction cosines from the normal to the basal plane and rotation around this axis:", anchor=tk.W)
		odf_v_lbl2.place(height=30,width=580,x=18,y=120)

		odf_v_lbl1_1_2 = tk.Label(odf_v, text="cos(x):\t           cos(y):\t\tcos(z): \t\t angle[degree]:", anchor=tk.W)
		odf_v_lbl1_1_2.place(height=20, width=570, x=18, y=150)


		odf_v_txt1 = tk.Entry(odf_v, text="")
		odf_v_txt2 = tk.Entry(odf_v, text="")
		odf_v_txt3 = tk.Entry(odf_v, text="")
		odf_v_txt4 = tk.Entry(odf_v, text="")
		odf_v_txt5 = tk.Entry(odf_v, text="")

		odf_v_txt1.place(height=20, width=50, x=65, y=150)
		odf_v_txt2.place(height=20, width=50, x=175, y=150)
		odf_v_txt3.place(height=20, width=50, x=330, y=150)
		odf_v_txt4.place(height=20, width=50, x=510, y=150)
		odf_v_txt5.place(height=20, width=50, x=100, y=185)

		odf_v_txt1.insert(tk.END, '0')
		odf_v_txt2.insert(tk.END, '0')
		odf_v_txt3.insert(tk.END, '1')
		odf_v_txt4.insert(tk.END, '0')
		odf_v_txt5.insert(tk.END, '0')

		odf_v_lbl3=tk.Label(odf_v,text="Mosaicity:", anchor=tk.W)
		odf_v_lbl3.place(height=30,width=80,x=18,y=180)

		inst_v_lbl2 = tk.Label(inst_v, text="Instrument Information:", anchor=tk.W,font=("Arial", 14))
		inst_v_lbl2.place(height=30, width=300, x=5, y=10)

		inst_v_radVar2=tk.IntVar() #Instrument

		def clkrad_2():
			if inst_v_radVar2.get()==3:
				inst_v_btn1=tk.Button(inst_v,text="Load",command=inst_v_clks1,state=tk.NORMAL)
				inst_v_btn1.place(height=30,width=50,x=300,y=65)
			else:
				inst_v_btn1=tk.Button(inst_v,text="Load",command=inst_v_clks1,state=tk.DISABLED)
				inst_v_btn1.place(height=30,width=50,x=300,y=65)


		inst_v_rad1=tk.Radiobutton(inst_v,text="ENGINX",variable=inst_v_radVar2,value=1,anchor=tk.W,command=clkrad_2)
		inst_v_rad1.place(height=30,width=80,x=5,y=35)

		inst_v_rad2=tk.Radiobutton(inst_v,text="IMAT",variable=inst_v_radVar2,value=2,anchor=tk.W,command=clkrad_2)
		inst_v_rad2.place(height=30,width=70,x=90,y=35)

		inst_v_rad2=tk.Radiobutton(inst_v,text="ASTOR (Still in development)",variable=inst_v_radVar2,value=4,anchor=tk.W,command=clkrad_2)
		inst_v_rad2.place(height=30,width=250,x=180,y=35)

		inst_v_rad3=tk.Radiobutton(inst_v,text="Add a new instrument",variable=inst_v_radVar2,value=3,anchor=tk.W,command=clkrad_2)
		inst_v_rad3.place(height=30,width=180,x=100,y=62)

		inst_v_radVar2.set(1)

		def inst_v_clks1():
		    a=1
		    ## Falta esto, xd

		inst_v_btn1=tk.Button(inst_v,text="Load",command=inst_v_clks1,state=tk.DISABLED)
		inst_v_btn1.place(height=30,width=50,x=300,y=62)

		inst_v_lbl1_1 = tk.Label(inst_v, text="Neutron beam direction:", anchor=tk.W)
		inst_v_lbl1_1.place(height=30, width=160, x=15, y=100)

		inst_v_cmb2=ttk.Combobox(inst_v, values=["Z axis","Y axis","X axis"])
		inst_v_cmb2.place(height=25,width=70,x=195,y=100)
		if simulation.beam=="Z axis":
			inst_v_cmb2.current(0)
		elif simulation.beam=="Y axis":
			inst_v_cmb2.current(1)
		elif simulation.beam=="X axis":
			inst_v_cmb2.current(2)

		def inst_v_btn1_click():
			global ODF
			simulation.add_I(inst_v_radVar2.get())
			simulation.add_beam(inst_v_cmb2.get())
			ODF=cl.ODF(3)
			ODF.load_modes([odf_v_txt1.get(),odf_v_txt2.get(),odf_v_txt3.get(),odf_v_txt4.get(),odf_v_txt5.get()])
			exp_option()

		inst_v_btn1 = tk.Button(inst_v, text="Next", command=inst_v_btn1_click)
		inst_v_btn1.place(height=40, width=80, x=260, y=280)



		odf_v.tkraise()
		inst_v.tkraise()
	if New_exp_cmb2.get()=="Powder":
		exp_option()

wind2_radVar1=tk.BooleanVar()		

def wizard_modes ():
	global wind2_radVar1
	window_2=tk.Tk()
	window_2.geometry ('600x600')
	window_2.resizable(0,0)
	window_2.title("Import ODF")

	wind2_fr1 = tk.LabelFrame(window_2, text="Step 1:")
	wind2_fr1.place(height=200, width=600, x=0, y=0)

	wind2_lbl1=tk.Label(wind2_fr1,text="ODF Creation",font=("Arial", 16))
	wind2_lbl1.place(height=40,width=200,x=200,y=20)

	wind2_lbl2=tk.Label(wind2_fr1,text="Step 1: Select the available\n data to create an ODF")
	wind2_lbl2.place(height=50,width=250,x=30,y=80)



	##Step 2
	wind2_fr2 = tk.LabelFrame(window_2, text="Step 2:")
	wind2_fr2.place(height=200, width=600, x=0, y=200)

	wind2_lbl3=tk.Label(wind2_fr2,text="Step 2: The file to upload must have one of the allowed formats")
	wind2_lbl3.place(height=30,width=450,x=30,y=10)
	def wind2_cmb2_click(event):
		global wind2_txt1
		if wind2_cmb2.get()=="φ θ ψ weight" or wind2_cmb2.get()=="q0 q1 q2 q3 weight":
			wind2_txt1 = tk.Entry(wind2_fr2, text="",state=tk.NORMAL)
			wind2_txt1.place(height=25,width=50,x=420,y=83)
		else:
			wind2_txt1 = tk.Entry(wind2_fr2, text="",state=tk.DISABLED)
			wind2_txt1.place(height=25,width=50,x=420,y=83)

	wind2_cmb2=ttk.Combobox(wind2_fr2, values=["φ θ ψ weight radius","φ θ ψ weight","q0 q1 q2 q3 weight radius","q0 q1 q2 q3 weight"])
	wind2_cmb2.place(height=30,width=200,x=20,y=50)
	wind2_cmb2.bind("<<ComboboxSelected>>", wind2_cmb2_click)
	wind2_cmb2.current(1)
	wind2_lbl4=tk.Label(wind2_fr2,text="Angles in:")
	wind2_lbl4.place(height=30,width=80,x=250,y=45)
	wind2_lbl4_1=tk.Label(wind2_fr2,text="Radius[degrees]:")
	wind2_lbl4_1.place(height=30,width=130,x=250,y=80)
	
	def wind2_radVar1_click1():
		global wind2_radVar1
		wind2_radVar1.set(True)
	def wind2_radVar1_click2():
		global wind2_radVar1
		wind2_radVar1.set(False)

	BI_rad1=tk.Radiobutton(wind2_fr2,text="Degree",variable=wind2_radVar1,value=True,anchor=tk.W,command=wind2_radVar1_click1)
	BI_rad1.place(height=30,width=100,x=350,y=45)
	BI_rad2=tk.Radiobutton(wind2_fr2,text="Radians",variable=wind2_radVar1,value=False,anchor=tk.W,command=wind2_radVar1_click2)
	BI_rad2.place(height=30,width=100,x=470,y=45)
	wind2_txt1 = tk.Entry(wind2_fr2, text="")
	wind2_txt1.place(height=25,width=50,x=420,y=83)

	##step 2_ Fourrier
	wind2_fr3 = tk.LabelFrame(window_2, text="Step 2:")
	wind2_fr3.place(height=200, width=600, x=0, y=200)

	wind2_lbl5=tk.Label(wind2_fr3,text="Step 2: Load the file with the Fourier coefficients")
	wind2_lbl5.place(height=30,width=350,x=30,y=30)

	def wind2_btn1_click():
		wind2_fr2.tkraise()
	def wind2_btn2_click():
		wind2_fr3.tkraise()
			
	
	wind2_btn1 = tk.Button(wind2_fr1, text="Modes in Euler space", command=wind2_btn1_click)
	wind2_btn1.place(height=30, width=150, x=310, y=70)

	wind2_btn2 = tk.Button(wind2_fr1, text="Fourier coefficients", command=wind2_btn2_click)
	wind2_btn2.place(height=30, width=150, x=310, y=110)

	wind2_fr2_1 = tk.LabelFrame(window_2, text="Step 2:")
	wind2_fr2_1.place(height=400, width=600, x=0, y=200)

	wind2_fr4 = tk.LabelFrame(window_2, text="Step 3:")
	wind2_fr4.place(height=200, width=600, x=0, y=400)

	wind2_lbl6=tk.Label(wind2_fr4,text="The ODF was loaded successfully",font=("Arial", 16))
	wind2_lbl6.place(height=30,width=400,x=100,y=10)

	wind2_lbl7=tk.Label(wind2_fr4,text="Save by the name:\n (allow use in future project) \n  or Follow withour saving\n ",anchor=tk.W)
	wind2_lbl7.place(height=80,width=200,x=50,y=50)

	wind2_txt2 = tk.Entry(wind2_fr4, text="")
	wind2_txt2.place(height=30,width=120,x=280,y=60)

	def wind2_btn5_click():
		if wind2_txt2.get!="":
			file = "ODF_data_base/" + wind2_txt2.get() + ".pkl"
			ODF.save(file)
		window_2.quit()
		window_2.destroy()
		inst_inf()


	wind2_btn5 = tk.Button(wind2_fr4, text="Save", command=wind2_btn5_click)
	wind2_btn5.place(height=30, width=70, x=310, y=110)



	def wind2_btn3_click():
		global ODF
		#try:
		ODF= cl.ODF(1)
		file = filedialog.askopenfilename(title="Select name", filetypes=(("Text files", "*.txt"), ("Data files", "*.dat")))
		data =open(file,"r")
		lines=data.readlines()
		modes=[]
		for ii in lines:
			aux=ii.split("\t")
			if len (aux)==1:
				aux=ii.split(" ")
			aux2=[]
			for jj in aux:
				if jj!=" ":
					aux2.append(jj)
			if wind2_cmb2.get()=="φ θ ψ weight" or wind2_cmb2.get()=="q0 q1 q2 q3 weight":
				r=wind2_txt1.get()
				aux2.append(r)
			if wind2_radVar1.get()==True:
				aux2[0]=float(aux2[0])*np.pi/180
				aux2[1]=float(aux2[1])*np.pi/180
				aux2[2]=float(aux2[2])*np.pi/180
			modes.append(aux2)
		ODF.load_modes(modes)
		wind2_fr4.tkraise()

		#except:
			#tk.messagebox.showinfo('Error: Invalid file',
             #                      "Please, make sure the format of the file is allowed")

	def wind2_btn4_click():
		global ODF
		#try:
		ODF= cl.ODF(2)
		file = filedialog.askopenfilename(title="Select name", filetypes=(("Text files", "*.txt"), ("Data files", "*.dat")))
		data =open(file,"r")
		lines=data.readlines()
		modes=[]
		for ii in lines:
			aux=ii.split(" ")
			aux2=[]
			for jj in aux:
				try:
					aux2.append(float(jj))
				except:
					asd=1
			modes.append(aux2)
		ODF.load_modes(modes)
		wind2_fr4.tkraise()
		#except:
		#	tk.messagebox.showinfo('Error: Invalid file',
         #                          "Please, make sure the format of the file is allowed")

	wind2_btn3 = tk.Button(wind2_fr2, text="Load", command=wind2_btn3_click)
	wind2_btn3.place(height=50, width=70, x=265, y=120)

	wind2_btn4 = tk.Button(wind2_fr3, text="Load", command=wind2_btn4_click)
	wind2_btn4.place(height=50, width=70, x=265, y=120)


	wind2_fr2_1.tkraise()
	wind2_fr1.tkraise()
	window_2.mainloop()

def inst_inf():

	inst_v_lbl2 = tk.Label(inst_v, text="Instrument Information:", anchor=tk.W,font=("Arial", 14))
	inst_v_lbl2.place(height=30, width=300, x=5, y=10)

	inst_v_radVar2=tk.IntVar() #Instrument

	def clkrad_2():
		if inst_v_radVar2.get()==3:
			inst_v_btn1=tk.Button(inst_v,text="Load",command=inst_v_clks1,state=tk.NORMAL)
			inst_v_btn1.place(height=30,width=50,x=300,y=65)
		else:
			inst_v_btn1=tk.Button(inst_v,text="Load",command=inst_v_clks1,state=tk.DISABLED)
			inst_v_btn1.place(height=30,width=50,x=300,y=65)


	inst_v_rad1=tk.Radiobutton(inst_v,text="ENGINX",variable=inst_v_radVar2,value=1,anchor=tk.W,command=clkrad_2)
	inst_v_rad1.place(height=30,width=80,x=5,y=35)

	inst_v_rad2=tk.Radiobutton(inst_v,text="IMAT",variable=inst_v_radVar2,value=2,anchor=tk.W,command=clkrad_2)
	inst_v_rad2.place(height=30,width=70,x=90,y=35)

	inst_v_rad2=tk.Radiobutton(inst_v,text="ASTOR (Still in development)",variable=inst_v_radVar2,value=4,anchor=tk.W,command=clkrad_2)
	inst_v_rad2.place(height=30,width=250,x=180,y=35)

	inst_v_rad3=tk.Radiobutton(inst_v,text="Add a new instrument",variable=inst_v_radVar2,value=3,anchor=tk.W,command=clkrad_2)
	inst_v_rad3.place(height=30,width=180,x=100,y=62)

	inst_v_radVar2.set(1)

	def inst_v_clks1():
	    a=1
	    ## Falta esto, xd

	inst_v_btn1=tk.Button(inst_v,text="Load",command=inst_v_clks1,state=tk.DISABLED)
	inst_v_btn1.place(height=30,width=50,x=300,y=62)

	inst_v_lbl1_1 = tk.Label(inst_v, text="Neutron beam direction:", anchor=tk.W)
	inst_v_lbl1_1.place(height=30, width=160, x=15, y=100)

	inst_v_cmb2=ttk.Combobox(inst_v, values=["Z axis","Y axis","X axis"])
	inst_v_cmb2.place(height=25,width=70,x=195,y=100)
	if simulation.beam=="Z axis":
		inst_v_cmb2.current(0)
	elif simulation.beam=="Y axis":
		inst_v_cmb2.current(1)
	elif simulation.beam=="X axis":
		inst_v_cmb2.current(2)

	def inst_v_btn1_click():
		global ODF
		simulation.add_I(inst_v_radVar2.get())
		simulation.add_beam(inst_v_cmb2.get())
		exp_option()

	inst_v_btn1 = tk.Button(inst_v, text="Next", command=inst_v_btn1_click)
	inst_v_btn1.place(height=40, width=80, x=260, y=280)

		#
	inst_v.tkraise()

def exp_option():
	#"Sample rotations","Samples with spatial resolution","Temperature variations","Transmission images"
	if New_exp_cmb1.get()=="Sample rotations":
		exp_sample_rot()
		exp_v.tkraise()
	if New_exp_cmb1.get()=="Temperature variations":
		exp_temp_var()
		exp_t.tkraise()
	if New_exp_cmb1.get()=="Transmission images":
		exp_trans_im()
		exp_i.tkraise()


##experimental global data
exp_v_cols=('#','φ','θ','ψ','α','β','l')
exp_v_txt9=tk.Entry(exp_v,text="")
exp_v_tree1=ttk.Treeview(exp_v,columns=exp_v_cols,show='headings')

exp_t_cols=('#','T','[]','l')
exp_t_tree1=ttk.Treeview(exp_t,columns=exp_t_cols,show='headings')

exp_i_cols=('Image','Pixel','λ')
exp_i_tree1=ttk.Treeview(exp_i,columns=exp_i_cols,show='headings')

def exp_sample_rot():
	global exp_v_txt9, exp_v_tree1 
	exp_v_lbl1 = tk.Label(exp_v, text="Sample Rotation",font=("Arial", 16))
	exp_v_lbl1.place(height=50, width=300, x=150, y=5)

	exp_v_lbl2 = tk.Label(exp_v, text="In this simulation, spectra will be obtained for each \n rotation proposed in this step")
	exp_v_lbl2.place(height=40, width=500, x=50, y=45)

	if geometry.type=="1":
		exp_v_lbl3 = tk.Label(exp_v, text="Since no geometry was defined, it's necessary \n to define the length of the neutron path \n in the sample or a value of [1cm]\n will be used by default.")
		exp_v_lbl3.place(height=80, width=500, x=50, y=90)
		exp_v_lbl10=tk.Label(exp_v,text="Neutron path in the sample:",anchor=tk.W)
		exp_v_lbl10.place(height=30,width=200,x=5,y=290)
		exp_v_txt10=tk.Entry(exp_v,text="")
		exp_v_txt10.place(height=20,width=60,x=195,y=295)
		exp_v_txt10.insert(tk.END, '1')

	else:
		exp_v_lbl3 = tk.Label(exp_v, text="Since geometry was defined,  \n can be choose the beam size or \n a default value of 1x1[mm] will be set")
		exp_v_lbl3.place(height=60, width=500, x=50, y=90)
		if simulation.beam=="Z axis":
			exp_v_lbl3_1 = tk.Label(exp_v, text="Δx:\t\tΔy:\t\t[mm]",anchor=tk.W)
			exp_v_lbl3_1.place(height=25, width=400, x=50, y=160)
		elif simulation.beam=="Y axis":
			exp_v_lbl3_1 = tk.Label(exp_v, text="Δx:\t\tΔz:\t\t[mm]",anchor=tk.W)
			exp_v_lbl3_1.place(height=25, width=400, x=50, y=160)
		elif simulation.beam=="X axis":
			exp_v_lbl3_1 = tk.Label(exp_v, text="Δy:\t\tΔz:\t\t[mm]",anchor=tk.W)
			exp_v_lbl3_1.place(height=25, width=400, x=50, y=160)
		exp_v_txt1 = tk.Entry(exp_v, text="")
		exp_v_txt1.place(height=25, width=70, x=80, y=160)
		exp_v_txt2 = tk.Entry(exp_v, text="")
		exp_v_txt2.place(height=25, width=70, x=200, y=160)
		exp_v_txt1.insert(tk.END, '1')
		exp_v_txt2.insert(tk.END, '1')


	exp_v_lbl2_1 = tk.Label(exp_v, text="Rotations information:", anchor=tk.W,font=("Arial", 14))
	exp_v_lbl2_1.place(height=30, width=300, x=5, y=205)

	exp_v_lbl4=tk.Label(exp_v,text="Define rotation by:",anchor=tk.W)
	exp_v_lbl4.place(height=30,width=180,x=5,y=235)

	exp_v_lbl5=tk.Label(exp_v,text="φ:",anchor=tk.W)
	exp_v_lbl5.place(height=30,width=25,x=10,y=265)
	exp_v_lbl6=tk.Label(exp_v,text="θ:",anchor=tk.W)
	exp_v_lbl6.place(height=30,width=25,x=100,y=265)
	exp_v_lbl7=tk.Label(exp_v,text="ψ:",anchor=tk.W)
	exp_v_lbl7.place(height=30,width=25,x=190,y=265)

	exp_v_txt7=tk.Entry(exp_v,text="")
	exp_v_txt7.place(height=20,width=55,x=30,y=271)
	exp_v_txt8=tk.Entry(exp_v,text="")
	exp_v_txt8.place(height=20,width=55,x=122,y=271)
	exp_v_txt9.place(height=20,width=55,x=210,y=271)

	exp_v_txt7.insert(tk.END, '0')
	exp_v_txt8.insert(tk.END, '0')
	exp_v_txt9.insert(tk.END, '0')


	def clk_exp_v_cmb1(event):
		global exp_v_lbl5,exp_v_lbl6,exp_v_lbl7,exp_v_txt9
		if exp_v_cmb1.get()=="euler angles in the laboratory system" or exp_v_cmb1.get()=="euler angles in the sample system":
			exp_v_txt9.place(height=20,width=55,x=210,y=271)
			exp_v_lbl5=tk.Label(exp_v,text="φ:",anchor=tk.W)
			exp_v_lbl5.place(height=30,width=25,x=10,y=265)
			exp_v_lbl6=tk.Label(exp_v,text="θ:",anchor=tk.W)
			exp_v_lbl6.place(height=30,width=25,x=100,y=265)
			exp_v_lbl7=tk.Label(exp_v,text="ψ:",anchor=tk.W)
			exp_v_lbl7.place(height=30,width=25,x=190,y=265)
		if exp_v_cmb1.get()=="α and β in the sample system":
			exp_v_txt9.place(height=0,width=0,x=0,y=0)
			exp_v_lbl5=tk.Label(exp_v,text="α:",anchor=tk.W)
			exp_v_lbl5.place(height=30,width=25,x=10,y=265)
			exp_v_lbl6=tk.Label(exp_v,text="β:",anchor=tk.W)
			exp_v_lbl6.place(height=30,width=25,x=100,y=265)
			exp_v_lbl7=tk.Label(exp_v,text="    ",anchor=tk.W)
			exp_v_lbl7.place(height=30,width=25,x=190,y=265)


	exp_v_cmb1=ttk.Combobox(exp_v, values=["euler angles in the laboratory system","euler angles in the sample system","α and β in the sample system"])
	exp_v_cmb1.bind("<<ComboboxSelected>>", clk_exp_v_cmb1)
	exp_v_cmb1.place(height=25,width=280,x=140,y=240)
	exp_v_cmb1.current(0)

	def exp_v_clks2():
		global exp_v_tree1
		if exp_v_cmb1.get()=="α and β in the sample system":
			try:
				a1=float(exp_v_txt7.get())
				a2=float(exp_v_txt8.get())
				if geometry.type=="1":
					try:
						a4=float(exp_v_txt10.get())
					except:
						a4=1
				else:
					a4="-"
				i=len(exp_v_tree1.get_children())        
				exp_v_tree1.insert("","end",iid=int(i),values=("ab",None,None,None,a1,a2,a4))
			except:
				messagebox.showinfo('Error: Not enough data','Please, we need the value of each angle')


		if exp_v_cmb1.get()=="euler angles in the laboratory system":
			try:
				a1=float(exp_v_txt7.get())
				a2=float(exp_v_txt8.get())
				a3=float(exp_v_txt9.get())
				if geometry.type=="1":
					try:
						a4=float(exp_v_txt10.get())
					except:
						a4=1
				else:
					a4="-"
				i=len(exp_v_tree1.get_children())        
				exp_v_tree1.insert("","end",iid=int(i),values=("LS",a1,a2,a3,None,None,a4))
			except:
				messagebox.showinfo('Error: Not enough data','Please, we need the value of each angle')

		if exp_v_cmb1.get()=="euler angles in the sample system":
			try:
				a1=float(exp_v_txt7.get())
				a2=float(exp_v_txt8.get())
				a3=float(exp_v_txt9.get())
				if geometry.type=="1":
					try:
						a4=float(exp_v_txt10.get())
					except:
						a4=1
				else:
					a4="-"
				i=len(exp_v_tree1.get_children())        
				exp_v_tree1.insert("","end",iid=int(i),values=("SS",a1,a2,a3,None,None,a4))
			except:
				messagebox.showinfo('Error: Not enough data','Please, we need the value of each angle')


        

	exp_v_btn2=tk.Button(exp_v,text="Save",command=exp_v_clks2)
	exp_v_btn2.place(height=35,width=70,x=340,y=280)

	
	exp_v_tree1.place(height=150,width=400,x=5,y=340)
	exp_v_tree1.column('#',width=-10,minwidth=0)
	exp_v_tree1.column('φ',width=55,minwidth=30)
	exp_v_tree1.column('θ',width=55,minwidth=30)
	exp_v_tree1.column('ψ',width=55,minwidth=30)
	exp_v_tree1.column('α',width=55,minwidth=30)
	exp_v_tree1.column('β',width=55,minwidth=30)
	exp_v_tree1.column('l',width=60,minwidth=30)
	for col in exp_v_cols:
		exp_v_tree1.heading(col,text=col)

	def exp_v_clks3():
		global exp_v_tree1

		aux=[]
		if len(exp_v_tree1.get_children())  ==0:
			if geometry.type=="1":
				a4=1
			else:
				a4="-"
			exp_v_tree1.insert("","end",iid=int(0),values=("-",0,0,0,0,0,a4))
		for ii in exp_v_tree1.get_children():
			aux.append(exp_v_tree1.item(ii,option="values"))
		try:
			a1=float(exp_v_txt1.get())
			a2=float(exp_v_txt2.get())
		except:
			a1=1
			a2=1
		simulation.add_B_I([a1,a2])
		simulation.add_rot(aux)
		simulation.add_material(material)
		simulation.add_geometry(geometry)
		simulation.add_ODF(ODF)
		aux=simulation
		project.add_simulation(aux)

		lststp.update(exp_v)
		final_option()
		
	exp_v_btn3=tk.Button(exp_v,text="Next",command=exp_v_clks3)
	exp_v_btn3.place(height=50,width=70,x=450,y=400)

def exp_temp_var():
	global exp_t_tree1
	exp_t_lbl1 = tk.Label(exp_t, text="Temperature variations",font=("Arial", 16))
	exp_t_lbl1.place(height=50, width=300, x=150, y=5)

	exp_t_lbl2 = tk.Label(exp_t, text="In this simulation, spectra will be obtained for each \n temperature proposed in this step")
	exp_t_lbl2.place(height=40, width=500, x=50, y=45)

	if geometry.type=="1":
		exp_t_lbl3 = tk.Label(exp_t, text="Since no geometry was defined, it's necessary \n to define the length of the neutron path \n in the sample or a value of [1cm]\n will be used by default.")
		exp_t_lbl3.place(height=80, width=500, x=50, y=90)
		exp_t_lbl10=tk.Label(exp_t,text="Neutron path in the sample:",anchor=tk.W)
		exp_t_lbl10.place(height=30,width=200,x=5,y=280)
		exp_t_txt10=tk.Entry(exp_t,text="")
		exp_t_txt10.place(height=20,width=60,x=195,y=285)
		exp_t_txt10.insert(tk.END, '1')

	else:
		exp_t_lbl3 = tk.Label(exp_t, text="Since geometry was defined,  \n can be choose the beam size or \n a default value of 1x1[mm] will be set")
		exp_t_lbl3.place(height=60, width=500, x=50, y=90)
		if simulation.beam=="Z axis":
			exp_t_lbl3_1 = tk.Label(exp_t, text="Δx:\t\tΔy:\t\t[mm]",anchor=tk.W)
			exp_t_lbl3_1.place(height=25, width=400, x=50, y=160)
		elif simulation.beam=="Y axis":
			exp_t_lbl3_1 = tk.Label(exp_t, text="Δx:\t\tΔz:\t\t[mm]",anchor=tk.W)
			exp_t_lbl3_1.place(height=25, width=400, x=50, y=160)
		elif simulation.beam=="X axis":
			exp_t_lbl3_1 = tk.Label(exp_t, text="Δy:\t\tΔz:\t\t[mm]",anchor=tk.W)
			exp_t_lbl3_1.place(height=25, width=400, x=50, y=160)
		exp_t_txt1 = tk.Entry(exp_t, text="")
		exp_t_txt1.place(height=25, width=70, x=80, y=160)
		exp_t_txt2 = tk.Entry(exp_t, text="")
		exp_t_txt2.place(height=25, width=70, x=200, y=160)
		exp_t_txt1.insert(tk.END, '1')
		exp_t_txt2.insert(tk.END, '1')

	exp_t_lbl2_1 = tk.Label(exp_t, text="Temperature information:", anchor=tk.W,font=("Arial", 14))
	exp_t_lbl2_1.place(height=30, width=300, x=5, y=205)

	exp_t_lbl4=tk.Label(exp_t,text="Insert temperature: \t\t[K]",anchor=tk.W)
	exp_t_lbl4.place(height=30,width=300,x=5,y=245)

	exp_t_txt3 = tk.Entry(exp_t, text="")
	exp_t_txt3.place(height=20, width=70, x=140, y=250)
	exp_t_txt3.insert(tk.END, '300')

	def exp_t_clks2():
		global exp_t_tree1
		try:
			a1=float(exp_t_txt3.get())
			if geometry.type=="1":
				try:
					a4=float(exp_t_txt10.get())
				except:
					a4=1
			else:
				a4="-"
			i=len(exp_t_tree1.get_children())        
			exp_t_tree1.insert("","end",iid=int(i),values=("T",a1,"K",a4))
		except:
			messagebox.showinfo('Error: Not enough data','Please, we need a valid temperature value')
       

	exp_t_btn2=tk.Button(exp_t,text="Save",command=exp_t_clks2)
	exp_t_btn2.place(height=35,width=70,x=330,y=265)

	exp_t_tree1.place(height=200,width=350,x=25,y=315)
	exp_t_tree1.column('#',width=50,minwidth=0)
	exp_t_tree1.column('T',width=150,minwidth=50)
	exp_t_tree1.column('[]',width=50,minwidth=50)
	exp_t_tree1.column('l',width=100,minwidth=50)
	for col in exp_t_cols:
		exp_t_tree1.heading(col,text=col)

	def exp_t_clks3():
		global exp_t_tree1

		aux=[]
		if len(exp_t_tree1.get_children())  ==0:
			if geometry.type=="1":
				a4=1
			else:
				a4="-"
			exp_t_tree1.insert("","end",iid=int(0),values=("T",300,'K',a4))
		for ii in exp_t_tree1.get_children():
			aux.append(exp_t_tree1.item(ii,option="values"))
		try:
			a1=float(exp_t_txt1.get())
			a2=float(exp_t_txt2.get())
		except:
			a1=1
			a2=1
		simulation.add_B_I([a1,a2])
		simulation.add_rot(aux)
		simulation.add_material(material)
		simulation.add_geometry(geometry)
		simulation.add_ODF(ODF)
		aux=simulation
		project.add_simulation(aux)

		lststp.update(exp_t)
		final_option()
		
	exp_t_btn3=tk.Button(exp_t,text="Next",command=exp_t_clks3)
	exp_t_btn3.place(height=50,width=70,x=450,y=400)

def exp_trans_im():
	global exp_i_tree1
	exp_i_lbl1 = tk.Label(exp_i, text="Transmission images",font=("Arial", 16))
	exp_i_lbl1.place(height=50, width=300, x=150, y=5)

	exp_i_lbl2 = tk.Label(exp_i, text="In this simulation, images will be obtained for each configuration.\n The size of the pixel and image can be changed\n as well the wavelength value for each image")
	exp_i_lbl2.place(height=60, width=500, x=50, y=45)

	aux=fun.minimos_maximos(geometry.get_points(),simulation.beam)
	if simulation.beam=="Z axis":
		
		aux2="The neutron beam was selected in the Z axis.\n The geometry definition have a range x=["+str(aux[0])+","+str(aux[1])+"][cm]\n and y=["+str(aux[2])+","+str(aux[3])+"][cm] (just remembering) "
		exp_i_lbl2_1 = tk.Label(exp_i, text=aux2)
		exp_i_lbl2_1.place(height=60, width=500, x=50, y=120)

		exp_i_lbl4=tk.Label(exp_i,text="Image size: \n x-range from:\t     to \t         [cm]\n y-range from:\t     to \t         [cm]",anchor=tk.W)
		exp_i_lbl4.place(height=70,width=400,x=5,y=245)
	if simulation.beam=="Y axis":
		
		aux2="The neutron beam was selected in the Y axis.\n The geometry definition have a range x=["+str(aux[0])+","+str(aux[1])+"][cm]\n and z=["+str(aux[2])+","+str(aux[3])+"][cm] (just remembering) "
		exp_i_lbl2_1 = tk.Label(exp_i, text=aux2)
		exp_i_lbl2_1.place(height=60, width=500, x=50, y=120)

		exp_i_lbl4=tk.Label(exp_i,text="Image size: \n x-range from:\t     to \t         [cm]\n z-range from:\t     to \t         [cm]",anchor=tk.W)
		exp_i_lbl4.place(height=70,width=400,x=5,y=245)
	if simulation.beam=="X axis":
		
		aux2="The neutron beam was selected in the X axis.\n The geometry definition have a range y=["+str(aux[0])+","+str(aux[1])+"][cm]\n and z=["+str(aux[2])+","+str(aux[3])+"][cm] (just remembering) "
		exp_i_lbl2_1 = tk.Label(exp_i, text=aux2)
		exp_i_lbl2_1.place(height=60, width=500, x=50, y=120)

		exp_i_lbl4=tk.Label(exp_i,text="Image size: \n x-range from:\t     to \t         [cm]\n z-range from:\t     to \t         [cm]",anchor=tk.W)
		exp_i_lbl4.place(height=70,width=400,x=5,y=245)

	exp_i_lbl2_1 = tk.Label(exp_i, text="Image information:", anchor=tk.W,font=("Arial", 14))
	exp_i_lbl2_1.place(height=30, width=300, x=5, y=200)

	exp_i_txt1 = tk.Entry(exp_i, text="")
	exp_i_txt1.place(height=20, width=50, x=100, y=270)
	exp_i_txt1.insert(tk.END, str(aux[0]))
	exp_i_txt2 = tk.Entry(exp_i, text="")
	exp_i_txt2.place(height=20, width=50, x=170, y=270)
	exp_i_txt2.insert(tk.END, str(aux[1]))

	exp_i_txt1_1 = tk.Entry(exp_i, text="")
	exp_i_txt1_1.place(height=20, width=50, x=100, y=290)
	exp_i_txt1_1.insert(tk.END, str(aux[0]))
	exp_i_txt2_1 = tk.Entry(exp_i, text="")
	exp_i_txt2_1.place(height=20, width=50, x=170, y=290)
	exp_i_txt2_1.insert(tk.END, str(aux[1]))

	exp_i_lbl5=tk.Label(exp_i,text="Pixel size:\t     x \t         [mm]",anchor=tk.W)
	exp_i_lbl5.place(height=30,width=400,x=5,y=315)

	exp_i_txt3 = tk.Entry(exp_i, text="")
	exp_i_txt3.place(height=20, width=60, x=90, y=320)
	exp_i_txt3.insert(tk.END, '1')
	exp_i_txt4 = tk.Entry(exp_i, text="")
	exp_i_txt4.place(height=20, width=60, x=170, y=320)
	exp_i_txt4.insert(tk.END, '1')

	exp_i_lbl6=tk.Label(exp_i,text="Wavelength:\t\t [A]",anchor=tk.W)
	exp_i_lbl6.place(height=30,width=400,x=5,y=345)

	exp_i_txt5 = tk.Entry(exp_i, text="")
	exp_i_txt5.place(height=20, width=60, x=90, y=350)
	exp_i_txt5.insert(tk.END, '4')

	exp_i_tree1.place(height=130,width=400,x=5,y=390)
	exp_i_tree1.column('Image',width=220,minwidth=50)
	exp_i_tree1.column('Pixel',width=130,minwidth=50)
	exp_i_tree1.column('λ',width=50,minwidth=50)
	for col in exp_i_cols:
		exp_i_tree1.heading(col,text=col)

	def exp_i_clks2():
		global exp_i_tree1
		try:
			a1=float(exp_i_txt1.get())
			a1_1=float(exp_i_txt1_1.get())
			a2=float(exp_i_txt2.get())
			a2_1=float(exp_i_txt2_1.get())
			a3=float(exp_i_txt3.get())
			a4=float(exp_i_txt4.get())
			a5=float(exp_i_txt5.get())
			i=len(exp_i_tree1.get_children())        
			exp_i_tree1.insert("","end",iid=int(i),values=(str(a1)+" to "+str(a2) +"x"+str(a1_1)+" to "+str(a2_1),str(a3)+"x"+str(a4),a5))
		except:
			messagebox.showinfo('Error: Not enough data','Please, we need valid values')
       

	exp_i_btn2=tk.Button(exp_i,text="Save",command=exp_i_clks2)
	exp_i_btn2.place(height=35,width=70,x=330,y=290)

	def exp_i_clks3():
		global exp_i_tree1

		aux=[]
		if len(exp_i_tree1.get_children())  ==0:
			try:
				a1=float(exp_i_txt1.get())
				a2=float(exp_i_txt2.get())
				a3=float(exp_i_txt3.get())
				a4=float(exp_i_txt4.get())
				a5=float(exp_i_txt5.get())
				i=len(exp_i_tree1.get_children())        
				exp_i_tree1.insert("","end",iid=int(i),values=(str(a1)+" to "+str(a2) +"x"+str(a1_1)+" to "+str(a2_1),str(a3)+"x"+str(a4),a5))
			except:
				messagebox.showinfo('Error: Not enough data','Please, we need valid values')
				return 0


		for ii in exp_i_tree1.get_children():
			aux.append(exp_i_tree1.item(ii,option="values"))
		

		
		simulation.add_rot(aux)
		simulation.add_material(material)
		simulation.add_geometry(geometry)
		simulation.add_ODF(ODF)
		aux=simulation
		project.add_simulation(aux)

		lststp.update(exp_i)
		final_option()
		
	exp_i_btn3=tk.Button(exp_i,text="Finish",command=exp_i_clks3)
	exp_i_btn3.place(height=50,width=70,x=450,y=400)

def final_option():
	#"Sample rotations","Samples with spatial resolution","Temperature variations","Transmission images"
	if project.name=="Sample rotations":
		final_rot()
		final_v.tkraise()
	if project.name=="Temperature variations":
		final_temp()
		final_t.tkraise()
	if project.name=="Transmission images":
		trans_ima()

def final_rot():
	final_v_lbl1 = tk.Label(final_v, text="Sample Rotation",font=("Arial", 16))
	final_v_lbl1.place(height=50, width=300, x=150, y=5)

	final_v_lbl2 = tk.Label(final_v, text="Were loaded "+str(len(simulation.rot))+" rotations. \n Finally, choose the wavelength range \n and the output parameters")
	final_v_lbl2.place(height=60, width=500, x=50, y=55)

	final_v_lbl3=tk.Label(final_v,text="Simulate from:\t\t to:\t \t [A]",anchor=tk.W)
	final_v_lbl3.place(height=30,width=400,x=10,y=160)

	final_v_lbl4 = tk.Label(final_v, text="Select parameter to print in the output *txt file\n and spectra to display in images")
	final_v_lbl4.place(height=50, width=500, x=50, y=190)
	
	final_v_txt4=tk.Entry(final_v,text="")
	final_v_txt5=tk.Entry(final_v,text="")
	final_v_txt4.place(height=25,width=65,x=120,y=163)
	final_v_txt5.place(height=25,width=65,x=230,y=163)

	final_v_txt4.insert(tk.END, "2")
	final_v_txt5.insert(tk.END, "9")

	final_v_var1=tk.BooleanVar() #Wavelength
	final_v_var2=tk.BooleanVar() #Energy
	final_v_var3=tk.BooleanVar() #"Transmission"
	final_v_var4=tk.BooleanVar() #"Total cross section"
	final_v_var5=tk.BooleanVar() #Elastic-coherent cross section (Bragg component)"
	final_v_var6=tk.BooleanVar() #show-"Transmission"
	final_v_var7=tk.BooleanVar() #show-Total cross section
	final_v_var8=tk.BooleanVar() #show-Elastic-coherent cross section (Bragg component)"

	final_v_ckbtn1=ttk.Checkbutton(final_v,text="Wavelength",variable=final_v_var1)
	final_v_ckbtn1.place(height=30, width=300, x=30, y=240)
	final_v_ckbtn2=ttk.Checkbutton(final_v,text="Energy",variable=final_v_var2)
	final_v_ckbtn2.place(height=30, width=300, x=30, y=280)
	final_v_ckbtn3=ttk.Checkbutton(final_v,text="Transmission",variable=final_v_var3)
	final_v_ckbtn3.place(height=30, width=300, x=30, y=320)
	final_v_ckbtn4=ttk.Checkbutton(final_v,text="Total cross section",variable=final_v_var4)
	final_v_ckbtn4.place(height=30, width=300, x=30, y=360)
	final_v_ckbtn5=ttk.Checkbutton(final_v,text="Elastic-coherent cross section (Bragg component)",variable=final_v_var5)
	final_v_ckbtn5.place(height=30, width=300, x=30, y=400)
	final_v_ckbtn6=ttk.Checkbutton(final_v,text="show",variable=final_v_var6)
	final_v_ckbtn6.place(height=30, width=100, x=400, y=320)
	final_v_ckbtn7=ttk.Checkbutton(final_v,text="show",variable=final_v_var7)
	final_v_ckbtn7.place(height=30, width=100, x=400, y=360)
	final_v_ckbtn8=ttk.Checkbutton(final_v,text="show",variable=final_v_var8)
	final_v_ckbtn8.place(height=30, width=100, x=400, y=400)


	def final_v_click3():
		files = [('Project File','*.pkl'),('All Files', '*.*')]
		file = asksaveasfile(filetypes = files, defaultextension = files)
		project.save_project(file.name)

	final_v_btn3=tk.Button(final_v,text="Save Project",command=final_v_click3)
	final_v_btn3.place(height=30,width=110,x=160,y=520)

	def final_v_click1():
		samp_rot([final_v_txt4.get(),final_v_txt5.get(),final_v_var1.get(),final_v_var2.get(),final_v_var3.get(),final_v_var4.get(),final_v_var5.get(),final_v_var6.get(),final_v_var7.get(),final_v_var8.get()])

	final_v_btn1=tk.Button(final_v,text="Run",command=final_v_click1)
	final_v_btn1.place(height=30,width=110,x=380,y=520)

def final_temp():
	final_t_lbl1 = tk.Label(final_t, text="Temperature variations",font=("Arial", 16))
	final_t_lbl1.place(height=50, width=300, x=150, y=5)

	final_t_lbl2 = tk.Label(final_t, text="Were loaded "+str(len(simulation.rot))+" temperature values. \n Finally, choose the wavelength range \n and the output parameters")
	final_t_lbl2.place(height=60, width=500, x=50, y=55)

	final_t_lbl3=tk.Label(final_t,text="Simulate from:\t\t to:\t \t [A]",anchor=tk.W)
	final_t_lbl3.place(height=30,width=400,x=10,y=160)

	final_t_lbl4 = tk.Label(final_t, text="Select parameter to print in the output *txt file\n and spectra to display in images")
	final_t_lbl4.place(height=50, width=500, x=50, y=190)
	
	final_t_txt4=tk.Entry(final_t,text="")
	final_t_txt5=tk.Entry(final_t,text="")
	final_t_txt4.place(height=25,width=65,x=120,y=163)
	final_t_txt5.place(height=25,width=65,x=230,y=163)

	final_t_txt4.insert(tk.END, "2")
	final_t_txt5.insert(tk.END, "9")

	final_t_var1=tk.BooleanVar() #Wavelength
	final_t_var2=tk.BooleanVar() #Energy
	final_t_var3=tk.BooleanVar() #"Transmission"
	final_t_var4=tk.BooleanVar() #"Total cross section"
	final_t_var5=tk.BooleanVar() #Elastic-coherent cross section (Bragg component)"
	final_t_var6=tk.BooleanVar() #show-"Transmission"
	final_t_var7=tk.BooleanVar() #show-Total cross section
	final_t_var8=tk.BooleanVar() #show-Elastic-coherent cross section (Bragg component)"

	final_t_ckbtn1=ttk.Checkbutton(final_t,text="Wavelength",variable=final_t_var1)
	final_t_ckbtn1.place(height=30, width=300, x=30, y=240)
	final_t_ckbtn2=ttk.Checkbutton(final_t,text="Energy",variable=final_t_var2)
	final_t_ckbtn2.place(height=30, width=300, x=30, y=280)
	final_t_ckbtn3=ttk.Checkbutton(final_t,text="Transmission",variable=final_t_var3)
	final_t_ckbtn3.place(height=30, width=300, x=30, y=320)
	final_t_ckbtn4=ttk.Checkbutton(final_t,text="Total cross section",variable=final_t_var4)
	final_t_ckbtn4.place(height=30, width=300, x=30, y=360)
	final_t_ckbtn5=ttk.Checkbutton(final_t,text="Elastic-coherent cross section (Bragg component)",variable=final_t_var5)
	final_t_ckbtn5.place(height=30, width=300, x=30, y=400)
	final_t_ckbtn6=ttk.Checkbutton(final_t,text="show",variable=final_t_var6)
	final_t_ckbtn6.place(height=30, width=100, x=400, y=320)
	final_t_ckbtn7=ttk.Checkbutton(final_t,text="show",variable=final_t_var7)
	final_t_ckbtn7.place(height=30, width=100, x=400, y=360)
	final_t_ckbtn8=ttk.Checkbutton(final_t,text="show",variable=final_t_var8)
	final_t_ckbtn8.place(height=30, width=100, x=400, y=400)


	def final_t_click3():
		files = [('Project File','*.pkl'),('All Files', '*.*')]
		file = asksaveasfile(filetypes = files, defaultextension = files)
		project.save_project(file.name)

	final_t_btn3=tk.Button(final_t,text="Save Project",command=final_t_click3)
	final_t_btn3.place(height=30,width=110,x=160,y=520)

	def final_t_click1():
		temp_var([final_t_txt4.get(),final_t_txt5.get(),final_t_var1.get(),final_t_var2.get(),final_t_var3.get(),final_t_var4.get(),final_t_var5.get(),final_t_var6.get(),final_t_var7.get(),final_t_var8.get()])

	final_t_btn1=tk.Button(final_t,text="Run",command=final_t_click1)
	final_t_btn1.place(height=30,width=110,x=380,y=520)

def samp_rot(data_out):
	for ii in project.simulation:
		if ii.beam=="Z axis":
			vector=[0,0,1]
		if ii.beam=="X axis":
			vector=[1,0,0]
		if ii.beam=="Y axis":
			vector=[0,1,0]
		lista=fun.Crear_Lista_hkl(ii.mat.struct,ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)
		v_0=fun.v_0(ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)
		for j,jj in enumerate(ii.rot):
			print("Rotacion=",j)
			if jj[0]=="-":
				r = R.from_euler('z', 0, degrees=True)
			else:
				if jj[0]=="ab":
					vector=[np.sin(float(jj[4])),np.cos(float(jj[4]))*np.cos(float(jj[5])),-np.cos(float(jj[4]))*np.sin(float(jj[5]))]
				if jj[0]=="LS":
					r=R.from_euler('zxz', [float(jj[1]),float(jj[2]),float(jj[3])], degrees=True)
					vector=r.apply(vector)
				if jj[0]=="SS":
					r=R.from_euler('zxz', [float(jj[1]),float(jj[2]),float(jj[3])], degrees=True)
					vector=r.apply(vector)
			print("vector=",vector)
			#Distancia
			if jj[6]=="-":
				aux=fun.minimos_maximos(ii.geo.get_points(),ii.beam)
				pixel=np.array(ii.B_I)*0.001
				if (aux[1]-aux[0])/pixel[0]>(aux[3]-aux[2])/pixel[1]:
					while ((aux[1]-aux[0])/pixel[0]*2>1000):
						pixel=pixel*2
					points=ii.geo.get_points(int((aux[1]-aux[0])/pixel[0]))
				else:
					while ((aux[3]-aux[2])/pixel[1]*2>1000):
						pixel=pixel*2
					points=ii.geo.get_points(int((aux[3]-aux[2])/pixel[1]*2))
				print("pixel=",pixel)

				x=np.reshape(points[0],(1,-1))
				y=np.reshape(points[1],(1,-1))
				z=np.reshape(points[2],(1,-1))
				for p,pp in enumerate(x[0]):
					aux=np.array([x[0][p],y[0][p],z[0][p]])
					aux=r.apply(aux)
					x[0][p]=aux[0]
					y[0][p]=aux[1]
					z[0][p]=aux[2]

				if ii.beam=="Z axis":
					point=[float(ii.B_I[0]),float(ii.B_I[1])]
					dist=fun.neutron_path_points(x[0],y[0],z[0],-pixel[0]/2,pixel[0]/2,-pixel[1]/2,pixel[1]/2,0)
					dist=dist[1]-dist[0]
				elif ii.beam=="X axis":
					point=[float(ii.B_I[1]),float(ii.B_I[2])]
					dist=fun.neutron_path_points(y[0],z[0],x[0],-pixel[0]/2,pixel[0]/2,-pixel[1]/2,pixel[1]/2,0)
					dist=dist[1]-dist[0]
				else:
					point=[float(ii.B_I[0]),float(ii.B_I[2])]
					dist=fun.neutron_path_points(x[0],z[0],y[0],-pixel[0]/2,pixel[0]/2,-pixel[1]/2,pixel[1]/2,0)
					dist=dist[1]-dist[0]
			else:
				dist=float(jj[6])
			print("Distancia=",dist)

			if float(data_out[1])-float(data_out[0])<2:		
				lam=np.linspace(float(data_out[0]), float(data_out[1]), num=100)
			else:
				lam=np.linspace(float(data_out[0]), float(data_out[1]), num=200)

			##NCrystal
			aux=cl.NCrystal_file(ii.mat.dir,300,lam)
			aux.save_Crystal_data()
			subprocess.call('./NCrystal_run.sh')
			aux.load_Ncrystal_data()
			data=aux.lam
			n=ii.mat.N/v_0
			print("Densidad volumetrica=",n)

			#output data
			energy=np.zeros(lam.shape[0])
			el=np.zeros(lam.shape[0])
			valor=np.zeros(lam.shape[0])
			tr=np.zeros(lam.shape[0])

			##

			if ii.ODF.type==0:
				print("Powder simulation")
				energy=np.array(data[1])
				el=np.array(data[3])			
				valor=np.array(data[2])
				tr=np.exp(-dist*n*(valor+el))
			elif ii.ODF.type==1:##Flor
				print("Flor algorithm")
				for k,kk in enumerate(ii.ODF.modes):
					r2=R.from_euler('zxz',[float(kk[0]),float(kk[1]),float(kk[2])])
					r2=r2.inv()
					vec_rot=r2.apply(vector)
					el+=float(kk[3])*fun.Simular_lam(lam,lista,vec_rot,v_0,ii.Ins,0.0001,(0.004)*np.pi/180,float(kk[4])*np.pi/180)
				energy=np.array(data[1])
				valor=np.array(data[2])
				tr=np.exp(-dist*n*(valor+el))
			
			elif ii.ODF.type==2:	##Miguel
				if fun.tipo_estructura(ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)==7:
					print("Estructura hexagonal")
					q=R.from_rotvec(np.pi/3*np.array([0,0,1]))
					b1=np.pi*2/v_0*ii.mat.c*ii.mat.a*np.array([1/2,np.sqrt(3)/2,0])
					b2=q.apply(b1)
					b3=2*np.pi/ii.mat.c*np.array([0,0,1])
				if fun.tipo_estructura(ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)==1:
					print("Estructura cubica")
					b1=2*np.pi/ii.mat.a*np.array([1,0,0])
					b2=2*np.pi/ii.mat.a*np.array([0,1,0])
					b3=2*np.pi/ii.mat.a*np.array([0,0,1])

				coef_four=np.zeros(len(ii.ODF.modes),dtype=complex)
				for k,kk in enumerate(ii.ODF.modes):
					coef_four[k]=complex(float(kk[3]),float(kk[4]))

				el=fun.simular_miguel(coef_four,lista,vector,v_0,b1,b2,b3,lam)
				energy=np.array(data[1])
				valor=np.array(data[2])
				tr=np.exp(-dist*n*(valor+el))

			elif ii.ODF.type==3:
				print ("Monocrystal")
				r2=R.from_rotvec(float(ii.ODF.modes[3])*np.array([float(ii.ODF.modes[0]),float(ii.ODF.modes[1]),float(ii.ODF.modes[2])]))
				r2=r2.inv()
				vec_rot=r2.apply(vector)
				el=fun.Simular_lam(lam,lista,vec_rot,v_0,ii.Ins,0.0001,(0.004)*np.pi/180,float(ii.ODF.modes[4])*np.pi/180)
				energy=np.array(data[1])
				valor=np.array(data[2])
				tr=np.exp(-dist*n*(valor+el))
			plot_samp_rot(j,lam,el,energy,valor,tr,data_out)

def plot_samp_rot(j,lam,el,energy,valor,tr,data_out):

	file=open("out/Data_"+str(j)+".txt",'w')
	for i,ii in enumerate(lam):
		aux1=""
		if data_out[2]:
			aux1+=str(lam[i])+"\t"
		if data_out[3]:
			aux1+=str(energy[i])+"\t"
		if data_out[4]:
			aux1+=str(tr[i])+"\t"
		if data_out[5]:
			aux1+=str(valor[i])+"\t"
		if data_out[6]:
			aux1+=str(el[i])+"\t"
		aux1+="\n"
		file.write(aux1)

	plt.figure(j)
	plt.xlabel('Wavelength [A]')
	plt.ylabel('Transmission')
	plt.legend(loc='upper right')

	if data_out[7]:
		plt.plot(lam,tr,label="Transmission")
		if data_out[8] or data_out[9]:
			plt.figure("Sec")
			plt.xlabel('Wavelength [A]')
			plt.ylabel('Cross sections [barns]')
			if data_out[8]:
				plt.plot(lam,valor,label="Total cross section")
			if data_out[9]:
				plt.plot(lam,el,label="Bragg component")
	else:
		if data_out[8] or data_out[9]:
			plt.xlabel('Wavelength [A]')
			plt.ylabel('Cross sections [barns]')
			if data_out[8]:
				plt.plot(lam,valor,label="Total cross section")
			if data_out[9]:
				plt.plot(lam,el,label="Bragg component")

	if data_out[7] or data_out[8] or data_out[9]:
		plt.show()

def temp_var(data_out):
	for ii in project.simulation:
		if ii.beam=="Z axis":
			vector=[0,0,1]
		if ii.beam=="X axis":
			vector=[1,0,0]
		if ii.beam=="Y axis":
			vector=[0,1,0]
		lista=fun.Crear_Lista_hkl(ii.mat.struct,ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)
		v_0=fun.v_0(ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)
		for j,jj in enumerate(ii.rot):
			print("Temperature=",jj)
			#Distancia
			if jj[3]=="-":
				aux=fun.minimos_maximos(ii.geo.get_points(),ii.beam)
				pixel=np.array(ii.B_I)*0.001
				if (aux[1]-aux[0])/pixel[0]>(aux[3]-aux[2])/pixel[1]:
					while ((aux[1]-aux[0])/pixel[0]*2>1000):
						pixel=pixel*2
					points=ii.geo.get_points(int((aux[1]-aux[0])/pixel[0]))
				else:
					while ((aux[3]-aux[2])/pixel[1]*2>1000):
						pixel=pixel*2
					points=ii.geo.get_points(int((aux[3]-aux[2])/pixel[1]*2))
				print("pixel=",pixel)

				x=np.reshape(points[0],(1,-1))
				y=np.reshape(points[1],(1,-1))
				z=np.reshape(points[2],(1,-1))
				for p,pp in enumerate(x[0]):
					aux=np.array([x[0][p],y[0][p],z[0][p]])
					aux=r.apply(aux)
					x[0][p]=aux[0]
					y[0][p]=aux[1]
					z[0][p]=aux[2]

				if ii.beam=="Z axis":
					point=[float(ii.B_I[0]),float(ii.B_I[1])]
					dist=fun.neutron_path_points(x[0],y[0],z[0],-pixel[0]/2,pixel[0]/2,-pixel[1]/2,pixel[1]/2,0)
				elif ii.beam=="X axis":
					point=[float(ii.B_I[1]),float(ii.B_I[2])]
					dist=fun.neutron_path_points(y[0],z[0],x[0],-pixel[0]/2,pixel[0]/2,-pixel[1]/2,pixel[1]/2,0)
				else:
					point=[float(ii.B_I[0]),float(ii.B_I[2])]
					dist=fun.neutron_path_points(x[0],z[0],y[0],-pixel[0]/2,pixel[0]/2,-pixel[1]/2,pixel[1]/2,0)
			else:
				dist=float(jj[3])
			print("Distancia=",dist)

			if float(data_out[1])-float(data_out[0])<2:		
				lam=np.linspace(float(data_out[0]), float(data_out[1]), num=100)
			else:
				lam=np.linspace(float(data_out[0]), float(data_out[1]), num=200)

			##NCrystal
			aux=cl.NCrystal_file(ii.mat.dir,j,lam)
			aux.save_Crystal_data()
			subprocess.call('./NCrystal_run.sh')
			aux.load_Ncrystal_data()
			data=aux.lam
			n=ii.mat.N/v_0
			print("Densidad volumetrica=",n)

			#output data
			energy=np.zeros(lam.shape[0])
			el=np.zeros(lam.shape[0])
			valor=np.zeros(lam.shape[0])
			tr=np.zeros(lam.shape[0])

			##

			if ii.ODF.type==0:
				energy=np.array(data[1])
				el=np.array(data[3])
				valor=np.array(data[2])
				tr=np.exp(-dist*n*(valor+el))
			elif ii.ODF.type==1:##Flor
				print("Flor algorithm")
				for k,kk in enumerate(ii.ODF.modes):
					r2=R.from_euler('zxz',[float(kk[0]),float(kk[1]),float(kk[2])])
					r2=r2.inv()
					vec_rot=r2.apply(vector)
					el+=float(kk[3])*fun.Simular_lam(lam,lista,vec_rot,v_0,ii.Ins,0.0001,(0.004)*np.pi/180,float(kk[4])*np.pi/180)
				energy=np.array(data[1])
				valor=np.array(data[2])
				tr=np.exp(-dist*n*(valor+el))
			
			elif ii.ODF.type==2:	##Miguel
				if fun.tipo_estructura(ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)==7:
					print("Estructura hexagonal")
					q=R.from_rotvec(np.pi/3*np.array([0,0,1]))
					b1=np.pi*2/v_0*ii.mat.c*ii.mat.a*np.array([1/2,np.sqrt(3)/2,0])
					b2=q.apply(b1)
					b3=2*np.pi/ii.mat.c*np.array([0,0,1])
				if fun.tipo_estructura(ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)==1:
					print("Estructura cubica")
					b1=2*np.pi/ii.mat.a*np.array([1,0,0])
					b2=2*np.pi/ii.mat.a*np.array([0,1,0])
					b3=2*np.pi/ii.mat.a*np.array([0,0,1])

				coef_four=np.zeros(len(ii.ODF.modes),dtype=complex)
				for k,kk in enumerate(ii.ODF.modes):
					coef_four[k]=complex(float(kk[3]),float(kk[4]))

				el=fun.simular_miguel(coef_four,lista,vector,v_0,b1,b2,b3,lam)
				energy=np.array(data[1])
				valor=np.array(data[2])
				tr=np.exp(-dist*n*(valor+el))

			elif ii.ODF.type==3:
				print ("Monocrystal")
				r2=R.from_rotvec(float(ii.ODF.modes[3])*np.array([float(ii.ODF.modes[0]),float(ii.ODF.modes[1]),float(ii.ODF.modes[2])]))
				r2=r2.inv()
				vec_rot=r2.apply(vector)
				el=fun.Simular_lam(lam,lista,vec_rot,v_0,ii.Ins,0.0001,(0.004)*np.pi/180,float(ii.ODF.modes[4])*np.pi/180)
				energy=np.array(data[1])
				valor=np.array(data[2])
				tr=np.exp(-dist*n*(valor+el))
			plot_temp_var(jj,lam,el,energy,valor,tr,data_out)
		
def plot_temp_var(j,lam,el,energy,valor,tr,data_out):

	file=open("out/Data_"+str(j)+".txt",'w')
	for i,ii in enumerate(lam):
		aux1=""
		if data_out[2]:
			aux1+=str(lam[i])+"\t"
		if data_out[3]:
			aux1+=str(energy[i])+"\t"
		if data_out[4]:
			aux1+=str(tr[i])+"\t"
		if data_out[5]:
			aux1+=str(valor[i])+"\t"
		if data_out[6]:
			aux1+=str(el[i])+"\t"
		aux1+="\n"
		file.write(aux1)

	plt.figure("Temperature="+str(j))
	plt.xlabel('Wavelength [A]')
	plt.ylabel('Transmission')
	plt.legend(loc='upper right')

	if data_out[7]:
		plt.plot(lam,tr,label="Transmission")
		if data_out[8] or data_out[9]:
			plt.figure("Temperature_sec="+str(j))
			plt.xlabel('Wavelength [A]')
			plt.ylabel('Cross sections [barns]')
			if data_out[8]:
				plt.plot(lam,valor,label="Total cross section")
			if data_out[9]:
				plt.plot(lam,el,label="Bragg component")
	else:
		if data_out[8] or data_out[9]:
			plt.xlabel('Wavelength [A]')
			plt.ylabel('Cross sections [barns]')
			if data_out[8]:
				plt.plot(lam,valor,label="Total cross section")
			if data_out[9]:
				plt.plot(lam,el,label="Bragg component")

	if data_out[7] or data_out[8] or data_out[9]:
		plt.show()

def trans_ima():
	for ii in project.simulation:
		if ii.beam=="Z axis":
			vector=[0,0,1]
		if ii.beam=="X axis":
			vector=[1,0,0]
		if ii.beam=="Y axis":
			vector=[0,1,0]
		lista=fun.Crear_Lista_hkl(ii.mat.struct,ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)
		v_0=fun.v_0(ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)
		for j,jj in enumerate(ii.rot):
			print("Imagen=",j)
			fig=plt.figure("Transmision "+jj[2])
			lam=float(jj[2])

			##NCrystal
			aux=cl.NCrystal_file(ii.mat.dir,j,[lam])
			aux.save_Crystal_data()
			subprocess.call('./NCrystal_run.sh')
			aux.load_Ncrystal_data()
			data=aux.lam
			n=ii.mat.N/v_0
			print("Densidad volumetrica=",n)


			el=0
			if ii.ODF.type==0:
				energy=np.array(data[1])
				el=np.array(data[3])
				valor=np.array(data[2])
			elif ii.ODF.type==1:##Flor
				print("Flor algorithm")
				for k,kk in enumerate(ii.ODF.modes):
					r2=R.from_euler('zxz',[float(kk[0]),float(kk[1]),float(kk[2])])
					r2=r2.inv()
					vec_rot=r2.apply(vector)
					el+=float(kk[3])*fun.Simular_lam([lam],lista,vec_rot,v_0,ii.Ins,0.0001,(0.004)*np.pi/180,float(kk[4])*np.pi/180)
				energy=np.array(data[1])
				valor=np.array(data[2])
			
			elif ii.ODF.type==2:	##Miguel
				if fun.tipo_estructura(ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)==7:
					print("Estructura hexagonal")
					q=R.from_rotvec(np.pi/3*np.array([0,0,1]))
					b1=np.pi*2/v_0*ii.mat.c*ii.mat.a*np.array([1/2,np.sqrt(3)/2,0])
					b2=q.apply(b1)
					b3=2*np.pi/ii.mat.c*np.array([0,0,1])
				if fun.tipo_estructura(ii.mat.a,ii.mat.b,ii.mat.c,ii.mat.alfa,ii.mat.beta,ii.mat.gamma)==1:
					print("Estructura cubica")
					b1=2*np.pi/ii.mat.a*np.array([1,0,0])
					b2=2*np.pi/ii.mat.a*np.array([0,1,0])
					b3=2*np.pi/ii.mat.a*np.array([0,0,1])

				coef_four=np.zeros(len(ii.ODF.modes),dtype=complex)
				for k,kk in enumerate(ii.ODF.modes):
					coef_four[k]=complex(float(kk[3]),float(kk[4]))

				el=fun.simular_miguel(coef_four,lista,vector,v_0,b1,b2,b3,[lam])
				energy=np.array(data[1])
				valor=np.array(data[2])
			elif ii.ODF.type==3:
				print ("Monocrystal")
				r2=R.from_rotvec(float(ii.ODF.modes[3])*np.array([float(ii.ODF.modes[0]),float(ii.ODF.modes[1]),float(ii.ODF.modes[2])]))
				r2=r2.inv()
				vec_rot=r2.apply(vector)
				el=fun.Simular_lam([lam],lista,vec_rot,v_0,ii.Ins,0.0001,(0.004)*np.pi/180,float(ii.ODF.modes[4])*np.pi/180)
				energy=np.array(data[1])
				valor=np.array(data[2])
				


			#Distancia

			aux=jj[0].split('x')
			aux1=aux[0].split(' to ')
			aux2=aux[1].split(' to ')
			image=np.array([float(aux1[0]),float(aux1[1]),float(aux2[0]),float(aux2[1])])

			aux=jj[1].split('x')
			pixel=np.array([float(aux[0])*0.001,float(aux[1])*0.001])

			zoom_1=(image[1]-image[0])/pixel[0]/200
			zoom_2=(image[3]-image[2])/pixel[1]/200
			print("zoom=",zoom_1,zoom_2)

			ax_1=np.arange(image[0]+pixel[0]/3,image[1]-pixel[0]/3,pixel[0])
			ax_2=np.arange(image[2]+pixel[1]/3,image[3]-pixel[1]/3,pixel[1])

			points=ii.geo.get_points(400)
			x=np.reshape(points[0],(1,-1))
			y=np.reshape(points[1],(1,-1))
			z=np.reshape(points[2],(1,-1))
			print(ax_1.shape[0],ax_2.shape[0])
			dist=np.zeros((ax_1.shape[0],ax_2.shape[0]))
			if ii.beam=="Z axis":
				for p,pp in enumerate(ax_1):
					print(p)
					for m,mm in enumerate(ax_2):
						dist_aux=fun.neutron_path_points(x[0],y[0],z[0],pp-zoom_1/2*pixel[0]/2,pp+zoom_1/2*pixel[0]/2,mm-zoom_2/2*pixel[1]/2,mm+zoom_2/2*pixel[1]/2,0)
						dist[p][m]=dist_aux[1]-dist_aux[0]
			
			elif ii.beam=="Y axis":
				for p,pp in enumerate(ax_1):
					print(p)
					for m,mm in enumerate(ax_2):
						dist_aux=fun.neutron_path_points(x[0],z[0],y[0],pp-zoom_1/2*pixel[0]/2,pp+zoom_1/2*pixel[0]/2,mm-zoom_2/2*pixel[1]/2,mm+zoom_2/2*pixel[1]/2,0)
						dist[p][m]=dist_aux[1]-dist_aux[0]

			elif ii.beam=="X axis":
				for p,pp in enumerate(ax_1):
					print(p)
					for m,mm in enumerate(ax_2):
						dist_aux=fun.neutron_path_points(y[0],z[0],x[0],pp-zoom_1/2*pixel[0]/2,pp+zoom_1/2*pixel[0]/2,mm-zoom_2/2*pixel[1]/2,mm+zoom_2/2*pixel[1]/2,0)
						dist[p][m]=dist_aux[1]-dist_aux[0]

			tr=np.exp(-dist*(valor+el)*n)

			#("out/imagen"+str(j)+".jpg",tr)
			



			plt.imshow(tr,cmap='gray',vmin=0,vmax=1)
			fig.savefig("out/imagen"+str(j)+".jpg")
			plt.show()

window.mainloop()
