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
        cursor.execute("SELECT created_at FROM warehousese WHERE warehouse_id = LAST_INSERT_ID()")
        created_time = cursor.fetchone()[0]
        db.commit()
        messagebox.showinfo("Success", f"Product added successfully\nCreated At: {created_time}")
    def update_warehouse(self):

        self.label = tk.Label(self.frame, text="What do you want to update?")
        self.label.pack()

        self.choice = ttk.Combobox(
            self.frame,
            values=["warehouse_name", "warehouse_location", "status"],
            state="readonly",
            width=47
        )
        self.choice.pack()

        self.label = tk.Label(self.frame, text="Enter warehouse ID")
        self.label.pack()
        self.houseID = tk.Entry(self.frame, width=50)
        self.houseID.pack()

        submit = tk.Button(self.frame, text="Next", command=self.open_update_window)
        submit.pack()


    def open_update_window(self):
        field = self.choice.get()
        warehouse_id = self.houseID.get()

        if field == "" or warehouse_id == "":
            messagebox.showerror("Error", "Please fill all fields")
            return

       
        self.new_window = tk.Toplevel(self.frame)
        self.new_window.title("Update " + field)

        tk.Label(self.new_window, text=f"Enter new {field}:").pack()

        self.newValue = tk.Entry(self.new_window, width=50)
        self.newValue.pack()

        tk.Button(self.new_window, text="Update", command=self.update).pack()


    def update(self):

        field = self.choice.get()
        warehouse_id = self.houseID.get()
        new_value = self.newValue.get()

        if new_value == "":
            messagebox.showerror("Error", "Please enter the new value")
            return

        sql = f"UPDATE warehouses SET {field}=%s WHERE warehouse_id=%s"
        cursor.execute(sql, (new_value, warehouse_id))
        db.commit()

        messagebox.showinfo("successfully", "Has been updated successfully")
        self.new_window.destroy()


    def delete_warehouse(self):
       name = tk.simpledialog.askstring("Delete Warehouse", "Enter the warehouse name to delete:")
       if not name:
          messagebox.showerror("Error", "Please enter a warehouse name")
          return

       cursor.execute("SELECT warehouse_id FROM warehouses WHERE warehouse_name=%s", (name,))
       result = cursor.fetchone()
       if not result:
          messagebox.showerror("Error", "Warehouse not found")
          return

       warehouse_id = result[0]

       cursor.execute("UPDATE warehouses SET deleted_at = NOW() WHERE warehouse_id=%s", (warehouse_id,))
       db.commit()

       cursor.execute("SELECT deleted_at FROM warehouses WHERE warehouse_id=%s", (warehouse_id,))
       deleted_time = cursor.fetchone()[0]

       messagebox.showinfo("Deleted", f"Warehouse '{name}' deleted successfully\nDeleted At: {deleted_time}")
