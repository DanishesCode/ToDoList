from tkinter import *
import customtkinter as CTk
import json

ButtonList = []
File = open("Config","r")
temp = File.read()
File.flush()
Data1 = json.loads(temp)

##Settings##
DefaultTheme = Data1["Theme"]
OpacityValue = int(Data1["Opacity"])


root = CTk.CTk()
root.title("To-Do List")
root.geometry("800x600")
root.resizable(False ,False)
root.attributes("-alpha",(OpacityValue/100))
CTk.set_default_color_theme("blue")
root._set_appearance_mode(DefaultTheme)


TaskList = []

def updateConfig(DefaultTheme,OpacityValue):
   if DefaultTheme == "":
    Data1.update(Opacity = OpacityValue)
   elif OpacityValue == "":
      Data1.update(Theme = DefaultTheme)
   f = open("Config","w")
   f.write(str(Data1).replace("'",'"'))
   f.close()
def updateTasksNum(TaskCounter):
   n = 0
   for i in TaskList:
      n +=1
   TaskCounter.configure(text = f"Tasks left: {n}")
def RemoveTask(Task,Button,TaskCounter):
   TaskList.remove(Task)
   File = open("Data","w")
   Str = ",".join(TaskList)
   File.write(Str)
   File.flush()
   Button.destroy()
   updateTasksNum(TaskCounter)
   
def AddTask(Entry,List,TaskCounter):
   Task = Entry.get()
   if Task == "" or Task == ",":
       print("Unsupported")
   else:
     TaskList.append(Task)
     File = open("Data","w")
     Str = ",".join(TaskList)
     File.write(Str)
     File.flush()
     item = CTk.CTkButton(List,width = 600,height = 80,text=Task,font=("Arial",30),hover = True,hover_color="#b03f56")
     item.configure(command=lambda task = Task,Button = item:RemoveTask(task,Button,TaskCounter ))
     ButtonList.append(item)
     item.pack(pady = 2)
     Entry.delete(0,END)
     updateTasksNum(TaskCounter)

def TaskSort(List,Parent):
   List = sorted(List,key=str.casefold)
   for i in Parent.winfo_children():
      i.destroy()
   for x in List:
      item = CTk.CTkButton(Parent,width = 600,height = 80,text=x,font=("Arial",30),hover = True,hover_color="#b03f56")
      item.configure(command=lambda task = x,Button = item:RemoveTask(task,Button,TaskCounter))
      item.pack(pady = 2)

def OpacityChanger(Value,Text,Root):
   Text.configure(text=f"Opacity: {round(Value)}%")
   root.attributes("-alpha",(Value/100))
   OpacityValue = Value
   updateConfig("",Value)

def ThemeChanger(Theme):
   root._set_appearance_mode(Theme)
   DefaultTheme = Theme
   updateConfig(Theme,"")




File = open("Data","r")
Data = File.readlines()
File.flush()
try:
 Data = Data[0]
 Data = Data.split(",")
 for i in Data:
     TaskList.append(i)
except:
   print("No data")



Label = CTk.CTkLabel(root,width = 800,height = 30,text="ToDo List",font=("Arial",30),bg_color="transparent")
Label.place(x=0,y=0)

Entry = CTk.CTkEntry(root,width = 400,height = 50,placeholder_text="Enter Task",text_color="white",bg_color="transparent")
Entry.place(x=100,y=50)

TaskCounter = CTk.CTkLabel(root,width = 90,height = 40,bg_color="transparent",text = "Task left: 0")
TaskCounter.place(x=670,y=325)

List = CTk.CTkScrollableFrame(root,width = 600,height = 400)
List.place(x= 20,y= 125)


AddButton = CTk.CTkButton(root,width = 100,height=55,text="Add",font=("Arial",40),command= lambda:AddTask(Entry,List,TaskCounter),hover_color="green")
AddButton.place(x= 525,y= 50)

ThemeOpt = CTk.CTkOptionMenu(root,width = 125,height=20,values = ["Dark","Light"],
                             command =ThemeChanger)
ThemeOpt.set(DefaultTheme)
ThemeOpt.place(x=655,y= 150)

SortButton = CTk.CTkButton(root,width = 125,height = 55,text = "Sort",font=("Arial",40),command = lambda:TaskSort(TaskList,List))
SortButton.place(x=655,y=200)

OpacityLabel = CTk.CTkLabel(root,width = 125,height=20,text=f"Opacity: {OpacityValue}%")
OpacityLabel.place(x= 655,y =275)

OpacitySlider = CTk.CTkSlider(root,width= 125, height = 20,from_=30,to = 100,number_of_steps=70,progress_color="transparent",
                              command  = lambda Value: OpacityChanger(Value,OpacityLabel,root))
OpacitySlider.set(OpacityValue)
OpacitySlider.place(x=655,y=300)


for i in TaskList:
    item = CTk.CTkButton(List,width = 600,height = 80,text=i,font=("Arial",30),hover = True,hover_color="#b03f56")
    item.configure(command=lambda task = i,Button = item:RemoveTask(task,Button,TaskCounter))
    item.pack(pady = 2)
    updateTasksNum(TaskCounter)
print("Start!")
root.mainloop()
