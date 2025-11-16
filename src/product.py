import tkinter as tk
import mysql.connector
from tkinter import messagebox
db = mysql.connector.connect(
    host="127.0.0.1", user="root", password="projectSW", database="work_man")
class product:
    def __init__(self,product_id,product_name,stats,quantaty):

      self.product_id=product_id
      self.product_name=product_name
      self.stats=stats
      self.quantaty=quantaty
      self.root=tk.Tk()
      self.root.title("adding a product")
      self.frame=tk.Frame(self.root,width=1000,height=1000)
      self.frame.pack()
      self.addProduct()
      self.root.mainloop()
    def adding_unadded_catagory(self):
       catagorys()
    def addProduct(self):
        self.label=tk.Label(self.frame,text="please enter the name of the new product ")
        self.label.pack(pady=5,padx=100)
        self.pname=tk.Entry(self.frame,width=50)
        self.pname.pack()
        #enter the price
        self.label=tk.Label(self.frame,text="please enter the price of the new product ")
        self.label.pack(pady=5,padx=100)
        self.price=tk.Entry(self.frame,width=50)
        self.price.pack()
        #adding producet stats
        self.label=tk.Label(self.frame,text="please enter the stats of the new product ")
        self.label.pack(pady=5,padx=100)
        self.stats=tk.Entry(self.frame,width=50)
        self.stats.pack()

        self.label = tk.Label(self.frame, text="Enter UOM (unit of measurement):")
        self.label.pack()
        self.uom = tk.Entry(self.frame, width=50)
        self.uom.pack()

        subment=tk.Button(self.frame,text="add the product in catagorry",command=self.adding_in_catagories)
        subment.pack()
    def adding_in_catagories(self):
        self.saving_pname=self.pname.get().strip()
        if not  self.saving_pname:
            messagebox.showwarning("please enter the product name")
            return 
        self.saving_price=self.price.get().strip()
        if not  self.saving_price:
            messagebox.showwarning("please enter the price")
            return 
        self.saving_stats=self.stats.get().strip()
        if not  self.saving_stats:
            messagebox.showwarning("please enter the stats")
            return 
        self.saving_uom = self.uom.get().strip()  
        if not self.saving_uom:
            messagebox.showerror("please enter the umo")
            return
        self.adding_window=tk.Toplevel(self.root)
        cursor = db.cursor()
        self.adding_window.title("addint product in a category")
        self.frame2=tk.Frame(self.adding_window,width=1000,height=1000)
        self.frame2.pack()
        self.label=tk.Label(self.frame2,text="enter the name of the catagorry")
        self.label.pack(pady=5,padx=5)
        self.enter_cat=tk.Entry(self.frame2,width=50)
        self.enter_cat.pack()
        subment=tk.Button(self.frame2,text="add the product in catagorry",command=self.save_in_database)
        subment.pack()
    def save_in_database(self):
        save_catName = self.enter_cat.get().strip()
        if not save_catName:
           messagebox.showwarning("Warning", "Please enter the category name")
           return
        cursor = db.cursor()
        sql = "SELECT categories_id FROM categories WHERE category_name=%s"
        cursor.execute(sql, (self.save_catName,))
        Cato_id = cursor.fetchone()
        if Cato_id:
            category_id = Cato_id[0]
            cursor.execute(
               "INSERT INTO products (product_name, price, status, category_id) VALUES (%s, %s, %s, %s)",
               (self.saving_pname, self.saving_price, self.saving_stats, category_id)
            )
            cursor.execute("SELECT created_at FROM products WHERE product_id = LAST_INSERT_ID()")
            created_time = cursor.fetchone()[0]
            db.commit()
            messagebox.showinfo("Success", f"Product added successfully\nCreated At: {created_time}")
            
        else:
           self.ask = tk.Label(self.frame2, text="Do you want to add a category?")
           self.ask.pack()

           yes_button = tk.Button(self.frame2, text="Yes", command=self.adding_unadded_catagory)
           yes_button.pack()

    def update_product_menu(self):
       self.update_win = tk.Toplevel(self.root)
       self.update_win.title("Update Product")

       frame = tk.Frame(self.update_win)
       frame.pack(padx=20, pady=20)

       tk.Label(frame, text="Choose what to update:").pack()

       self.update_choice = tk.StringVar()
       choices = [
        "product_name",
        "price",
        "status",
        "uom",
        "quantity",
        "category"
        ]

       self.box = tk.OptionMenu(frame, self.update_choice, *choices)
       self.box.pack()

       tk.Label(frame, text="Enter Product ID:").pack()
       self.update_pid = tk.Entry(frame, width=40)
       self.update_pid.pack()

       submit = tk.Button(frame, text="Continue", command=self.open_update_window)
       submit.pack(pady=10)


    def open_update_window(self):
       choice = self.update_choice.get()
       pid = self.update_pid.get().strip()

       if choice == "" or pid == "":
          messagebox.showerror("Error", "Please fill all fields")
          return

       self.final_update = tk.Toplevel(self.root)
       self.final_update.title("Update Value")

       frame = tk.Frame(self.final_update)
       frame.pack(padx=20, pady=20)

       if choice == "category":
           tk.Label(frame, text="Enter NEW category name:").pack()
       else:
           tk.Label(frame, text=f"Enter new value for {choice}:").pack()
       self.new_val = tk.Entry(frame, width=50)
       self.new_val.pack()
       tk.Button(frame, text="Save", command=self.save_product_update).pack(pady=10)

    def save_product_update(self):
       field = self.update_choice.get()
       pid = self.update_pid.get().strip()
       new_value = self.new_val.get().strip()

       if new_value == "":
           messagebox.showerror("Error", "New value cannot be empty")
           return

       cursor = db.cursor()

       if field == "category":
           cursor.execute("SELECT category_id FROM categories WHERE category_name=%s", (new_value,))
           result = cursor.fetchone()

           if not result:
               messagebox.showerror("Error", "Category does not exist")
               return

           cat_id = result[0]
           sql = "UPDATE products SET category_id=%s WHERE product_id=%s"
           cursor.execute(sql, (cat_id, pid))
           db.commit()
           messagebox.showinfo("Success", "Product category updated successfully")
       
           sql = f"UPDATE products SET {field}=%s WHERE product_id=%s"
           cursor.execute(sql, (new_value, pid))
           db.commit()
           messagebox.showinfo("Success", f"{field} updated successfully")

    def delete_product(self):
   
       name = tk.simpledialog.askstring("Delete Product", "Enter the product name to delete:")
       if not name:
          messagebox.showerror("Error", "Please enter a product name")
          return

   
       cursor.execute("SELECT product_id FROM products WHERE product_name=%s", (name,))
       result = cursor.fetchone()
       if not result:
          messagebox.showerror("Error", "Product not found")
          return

       product_id = result[0]

  
       cursor.execute("UPDATE products SET deleted_at = NOW() WHERE product_id=%s", (product_id,))
       db.commit()

    
       cursor.execute("SELECT deleted_at FROM products WHERE product_id=%s", (product_id,))
       deleted_time = cursor.fetchone()[0]

       messagebox.showinfo("Deleted", f"Product '{name}' deleted successfully\nDeleted At: {deleted_time}")
