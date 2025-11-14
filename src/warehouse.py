import tkinter as tk
from tkinter import messagebox 
import mysql.connector
class warehous:
    def __init__(self,warehouse_name,warehous_id,warehous_location,stats,capacity):
        self.warehouse_name=warehouse_name
        self.warehous_id=warehous_id
        self.warehous_location=warehous_location
        self.stats=stats
        self.capacity=capacity
        self.root=tk.Tk()
        self.root.title("warehouse")
        self.frame=tk.Frame(self.root,width=1000,hight=1000)
        self.frame.pack()
    def add_warhouse(self):
        self.label=tk.Label(self.frame,text="please enter the warehouse name")
        self.label.pack()
        self.houseN=tk.Entry(self.frame,width=50)
        self.houseN.pack()

        self.label=tk.Label(self.frame,text="please enter the warehouse location")
        self.label.pack()
        self.houseL=tk.Entry(self.frame,width=50)
        self.houseL.pack()

        self.label=tk.Label(self.frame,text="please enter the warehouse stats")
        self.label.pack()
        self.houseS=tk.Enrtry(self.frame,width=50)
        self.houseS.pack()

        submet=tk.Button(self.frame,text="submet",command=add_toWdatatbase)
    def add_maneger(self):
        self.new_window=Toplevel(self.root)
        self.frame2=tk.Frame(self.new_window,width=1000,height=1000)
        self.frame2.pack()
        self.label=tk.Label(self.frame2,text="pleas entre the maneger name")
        self.label.pack()
        self.manegerN=tk.Entry(self.frame2,width=50)
        self.manegerN
        submet=tk.Button(self.frame,text="submet",command=add__to_manegerDatabase)

    def add_toWdatatbase(self):
        house_name=self.houseN.get
        if not house_name:
            messagebox.showwarning("warning","please enter the warehouse name")
            return
        houes_location=self.houseL.get()
        if not house_location:
            messagebox.showwarning("warning","please enter the warehouse location")
            return
        house_status=self.houseS.get()
        if not house_status:
            messagebox.showwarning("warning","please enter the warehouse status")
            return
        croser=db.croser
        insert_sql="INSERT INTO warehaouses (warehouse_name,warehouse_location,capacity,status) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_sql, (house_name,houes_location,0,house_status ))
        db.commit()
        cursor.execute("SELECT warehouse_id FROM warehouses WHERE warehouse_name=%s", (house_names,))
        result = cursor.fetchone()
        if result:
            warehouse_id = result[0]
            update_sql="UPDATE warehouses SET capacity=capacity+1 WHERE warehouse_id=%s"
            croser.execute(update_sql,warehouse_id)
        db.commit()
        messagebox.showinfo("Success", "warehouse added successfully")
        addmaneger=tk.Button(self.frame,text="add maneger",command=add_maneger)
        def add__to_manegerDatabase(self):
            maneger_name=manegerN.get()
            if not maneger_name:
                messagebox.showwarning("warning","please enter the maneger name")
                return
        cursor.execute("SELECT maneger_id FROM warehouses WHERE maneger_name=%s", (maneger_names,))
        result2 = cursor.fetchone()
        if result2:
            maneger_id=result2[0]
            insert_name("INSERT INTO warehoueses (maneger_id) VALUES(%s,%s)")
            valuse=(insert_name,(result2,))
    def update_warehouse(self):
        self.label=tk.Label(self.frame,text="please enter the warehouse name")
        self.label.pack()
        self.houseN=tk.Entry(self.frame,width=50)
        self.houseN.pack()

        self.label=tk.Label(self.frame,text="please enter the warehouse location")
        self.label.pack()
        self.houseL=tk.Entry(self.frame,width=50)
        self.houseL.pack()

        self.label=tk.Label(self.frame,text="please enter the warehouse stats")
        self.label.pack()
        self.houseS=tk.Enrtry(self.frame,width=50)
        self.houseS.pack()

        submet=tk.Button(self.frame,text="submet",command=update)
    def update(self):

        sql = "UPDATE warehouses SET warehouse_name=%s, warehouse_location=%s, manager_id=%s, capacity=%s, status=%s WHERE warehouse_id=%s"
        cursor.execute(sql, (name, location, manager_id, capacity, status, warehouse_id))
        db.commit()
        messagebox.showinfo("seccesfully","ahve ben updated seccesfully")
    def delete_warehouse(warehouse_id):
        self.label=tk.Label(self.frame,text="please enter the warehouse name")
        self.label.pack()
        self.houseN=tk.Entry(self.frame,width=50)
        self.houseN.pack()

        self.label=tk.Label(self.frame,text="please enter the warehouse location")
        self.label.pack()
        self.houseL=tk.Entry(self.frame,width=50)
        self.houseL.pack()

        self.label=tk.Label(self.frame,text="please enter the warehouse stats")
        self.label.pack()
        self.houseS=tk.Enrtry(self.frame,width=50)
        self.houseS.pack()

        submet=tk.Button(self.frame,text="submet",command=update)
    def deleat(self):
       sql = "DELETE FROM warehouses WHERE warehouse_id=%s"
       cursor.execute(sql, (warehouse_id,))
       db.commit()
       messagebox.showinfo("seccesfully","ahve ben deleated seccesfully")
