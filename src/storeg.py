import tkinter as tk
from tkinter import messagebox
import mysql.connector
class storag_section:
    def __init__(self,section_id,section_name,capacity,status):
        self.status=status
        self.capcity=capacity
        self.section_id=section_id
        self.section_name=section_name
        self.root=tk.Tk()
        self.root.title("storag_section")
        self.frame=tk.Frame(self.root,width=1000,height=1000)
        self.frame.pack() 
        self.add_section()
        self.root.mainloop()
    def add_section(self):
        self.label=tk.Label(self.frame,text="enter the name of the section")
        self.label.pack()
        self.section_name=tk.Entry(self.frame, width=50)
        self.section_name.pack()
        self.label=tk.Label(self.frame,text="enter the name of the section")
        self.label.pack()
        self.status=tk.Entry(self.frame, width=50)
        self.status.pack()
        self.label=tk.Label(self.frame,text="enter the wherehouse that you want to add the section")
        self.label.pack()
        self.house=tk.Entry(self.frame,width=50)
        self.house.pack()
        self.capacity=0
        submet=tk.Button(self.frame,text="submet",command=self.adding_to_secdatabase)
    def adding_to_secdatabase(self):
       section_names = self.section_name.get().strip()
       if not section_names:
          messagebox.showwarning("Warning", "Please enter a section name")
          return
          statuse = self.status.get().strip()
       if not statuse:
          messagebox.showwarning("Warning", "Please enter the status")
          return
       wherehouse=self.house.get()
       if not wherehouse:
          messagebox.showwarning("Warning", "Please enter the wherehouse")
          return
        

       cursor = db.cursor()
       sql = "INSERT INTO storage_section (section_name,status,capacity) VALUES (%s,%s,%s)"
       cursor.execute(sql, (section_names,statuse,self.capacity,))
       cursor.execute("SELECT section_id FROM storage_section WHERE section_name=%s", (section_names,))
       result = cursor.fetchone()
       if result:
          section_id = result[0]
          update_sql = "UPDATE storage_section SET capacity = capacity + 1 WHERE section_id = %s"
          cursor.execute(update_sql, (section_id,))   
       warehouse_sql = "INSERT INTO warehouses (warehouse_name, section_name) VALUES (%s, %s)"
       cursor.execute(warehouse_sql, (wherehouse, section_names))
       db.commit()  
       messagebox.showinfo("Success", "it ben added seccesfully")

    def update_section(self):
        self.label=tk.Label(self.frame,text="enter the name of the section")
        self.label.pack()
        self.section_name=tk.Entry(self.frame, width=50)
        self.section_name.pack()
        self.label=tk.Label(self.frame,text="enter the name of the section")
        self.label.pack()
        self.status=tk.Entry(self.frame, width=50)
        self.status.pack()
        self.label=tk.Label(self.frame,text="enter the wherehouse that you want to add the section")
        self.label.pack()
        self.house=tk.Entry(self.frame,width=50)
        self.house.pack()
        submet=tk.Button(self.frame,text="submet",command=self.update)
    def update(self):
        sql = "UPDATE storage_sections SET warehouse_id=%s, section_name=%s, capacity=%s, status=%s ,section id"
        cursor.execute(sql, (warehouse_id, section_name, capacity, status, section_id))
        db.commit()
        messagebox.showinfo("Success", "it ben updated seccesfully")
    def delete_section(self):
        self.label=tk.Label(self.frame,text="enter the name of the section")
        self.label.pack()
        self.section_name=tk.Entry(self.frame, width=50)
        self.section_name.pack()
        self.label=tk.Label(self.frame,text="enter the name of the section")
        self.label.pack()
        self.status=tk.Entry(self.frame, width=50)
        self.status.pack()
        self.label=tk.Label(self.frame,text="enter the wherehouse that you want to add the section")
        self.label.pack()
        self.house=tk.Entry(self.frame,width=50)
        self.house.pack()
        submet=tk.Button(self.frame,text="submet",command=self.remove)
    def remove(self):
       sql = "DELETE FROM storage_sections WHERE section_id=%s"
       cursor.execute(sql, (section_id,))
       db.commit()
       messagebox.showinfo("Success", "it ben deleated seccesfully")

    
       
