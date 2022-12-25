
from pydoc import importfile
from tkinter import *
from tkinter import filedialog
import tkinter.font as font
from PIL import ImageTk,Image
import cv2
from detectDefect import detection


root = Tk()
root.title('Blister Package Defect Detection')
root.geometry("1400x700")
root.config(bg='#636664')

font_1 = font.Font(size=10,weight="bold")
font_2 = font.Font(size=20,weight="bold")
font_3 = font.Font(size=15,weight="bold")

title_label = Label(root,text="Blister Package Defect Detection",fg='white',bg='#636664',font=font_2)
title_label.grid(row=0,column=1,pady=20)

frame_template = Frame(root,height=350,width=350,bg="white")
frame_template.grid(row=1,column=0,padx=40,pady=50)
frame_blisterP = Frame(root,height=350,width=350,bg="white")
frame_blisterP.grid(row=1,column=1,padx=40,pady=50)
frame_detect = Frame(root,height=350,width=350,bg="white")
frame_detect.grid(row=1,column=2,padx=40,pady=50)

def template(image_path):
        global panelA
        global image_template
        if len(image_path) > 0:
                image_original = cv2.imread(image_path,cv2.IMREAD_COLOR)
                image_template = image_original

                image_org = cv2.resize(image_original,(300,340))
                image_rgb = cv2.cvtColor(image_org,cv2.COLOR_BGR2RGB)
        
                image = Image.fromarray(image_rgb)
                image = ImageTk.PhotoImage(image)

                if panelA is None:
                        panelA = Label(frame_template,image=image,relief=GROOVE)
                        panelA.image = image
                        panelA.pack(side="left", padx=10, pady=10)

                else:
                        panelA.config(image=image)
                        panelA.image = image   

def detect_blisters(image_path):
        global panelB
        global image_blister
        if len(image_path) > 0:
                image_original = cv2.imread(image_path,cv2.IMREAD_COLOR)
                image_blister = image_original

                image_org = cv2.resize(image_original,(300,340))
                image_rgb = cv2.cvtColor(image_org,cv2.COLOR_BGR2RGB)
        
                image = Image.fromarray(image_rgb)
                image = ImageTk.PhotoImage(image)

                if panelB is None:
                        panelB = Label(frame_blisterP,image=image,relief=GROOVE)
                        panelB.image = image
                        panelB.pack(side="left", padx=10, pady=10)
                else:
                        panelB.config(image=image)
                        panelB.image = image
                        
def select_template():
        path = filedialog.askopenfilename(initialdir="./images",title='Select Template')
        template(path) 

def select_blister_pack():
        path = filedialog.askopenfilename(initialdir="./images",title='Select Blister Pack')
        detect_blisters(path)

def detect_defects():
        global panelC
        detected_image,state = detection(image_template,image_blister)
        detected_image = cv2.resize(detected_image,(300,340))

        image = Image.fromarray(detected_image)
        image = ImageTk.PhotoImage(image)
        if panelC is None:
                panelC = Label(frame_detect,image=image,relief=GROOVE)
                panelC.image = image
                panelC.pack(side="left", padx=10, pady=10)
        else:
                panelC.config(image=image)
                panelC.image = image
        result_label = Label(root,text=state,fg='red',bg='#636664',font=font_3,width=15)
        result_label.grid(row=3,column=2,pady=10)

panelA = None
panelB = None
panelC = None

button_temp = Button(root,text='Select Template',height=2,width=18,bg="#aecad0",command=select_template)
button_temp['font'] = font_1
button_temp.grid(row=2,column=0)

button_blisterP = Button(root,text='Select Blister Pack',height=2,width=18,bg="#aecad0",command=select_blister_pack)
button_blisterP['font'] = font_1
button_blisterP.grid(row=2,column=1)

button_defectP = Button(root,text='Detect Defects',height=2,width=18,bg="#aecad0",command=detect_defects)
button_defectP['font'] = font_1
button_defectP.grid(row=2,column=2)



root.mainloop()

            
        
