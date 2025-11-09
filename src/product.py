import Tkinter as tk
import mysql.connector
root=tk()
root.title("adding a product")
frame=tk.frame(root,width=1000,height=1000)
frame.pack()
cursor = db.cursor()
class product(self,product_id,product_name,stats):
    self.product_id=product_id
    self.profuct_name=product_name
    self.stats=stats
    def addProduct():
        label=tk.Label(frame,text="please enter the name of the new product ")
        label.pack(pady=5,padx=100)
        pname=tk.entery(frame,width=50)
        pname.pack()
        self.profuct_name=pname.get().strip()
        save_pname=self.product
        #enter the price
        label=tk.Label(frame,text="please enter the price of the new product ")
        label.pack(pady=5,padx=100)
        price=tk.entery(frame,width=50)
        price.pack()
        saving_price=price.get().strip()
        #adding producet stase
        label=tk.Label(frame,text="please enter the stats of the new product ")
        label.pack(pady=5,padx=100)
        stats=tk.entery(frame,width=50)
        stats.pack()
        saving_stats=price.get().strip()
        subment=tk.button(frame,text="add the product in catagorry",command=adding_in_catagoies)
        
    def adding_in_catagories():
        if not  save_pname:
            messagebox.showwarning("please enter the product name")
            return 
        if not  save_price:
            messagebox.showwarning("please enter the price")
            return 
        if not  save_stats:
            messagebox.showwarning("please enter the stats")
            return 
        adding_window=tk.toplevel(root)
        cursor = db.cursor()
        adding_window.title("addint product in a category")
        frame2=tk.Frame(adding_window,width=1000,height=1000)
        frame.pack()
        label=tk.Label(frame2,text="enter the name of the catagorry")
        label.pack(pady=5,padx=5)
        enter_cat=tk.entry(frame2,width=50)
        enter_cat.pack()
        save_catName=enter_cat.get().strip()
        subment=tk.Button(frame,text="add the product in catagorry",command=save_in_database)
        def save_in_database():
            if not ave_catName:
                messagebox.showwarning("please enter the the catagorry name name")
                return
        sql=("sellect categories_id from categoreis where catagory_name=%s ")
        cursor.execute(sql,(save_catName,))
        Cat_id=cursor.fetchone()
        if Cat-id:
            cursor.execute(
        "INSERT INTO products (product_name, category_id, price, status) VALUES (%s, %s, %s, %s)",(save_pname ,Cat_id, save_price,save_stats))
        else:
            


