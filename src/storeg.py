from tkinter as tk
import mysql.connector
    
class storeg():
    def __init__(self,section_id):
        def __init
        self.opration=operation
    def the_opreration():
        print("enter waht do you want to do: ")
    def sellect_whrehouse():

    def sellectiong_section():
        croser=db.croser
        root=tk.TK()
        root.title("sellictiong section ")
        frame=tk.Frame(root,width=1000,height=1000)
        frame.pack()
        label=tk.Label(frame,text="sellictiong please enter youer section ID: ")
        label.pack(pady=5,padx=5)
        enter_ID=tk.entery(frame,width=100)
        enter_ID.pack()
        entered=enter_ID.get()
        cursor = db.cursor()
        qury="select warehouse_id FROM warehouses WHERE warehouse_name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        
