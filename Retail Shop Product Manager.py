from tkinter import *
from tkinter import messagebox
from beautifultable import BeautifulTable
import sqlite3
# Setup GUI and database
########################################################################################################################
root = Tk()
root.title("Retail Shop Product Location Manager")
icon = ""
root.iconbitmap(icon)
root.geometry("+0+0")


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('racking_product_info.db')
        self.cursor = self.conn.cursor()


db = DB()
########################################################################################################################
# Create new table
########################################################################################################################
create_frame = LabelFrame(root, text="Create new racking", padx=10, pady=10)
create_frame.grid(row=0, column=0)

ctf_name_label = Label(create_frame, text="Racking name : ", padx=5, pady=5)
ctf_name_label.grid(row=0, column=0)

ctf_entry = Entry(create_frame)
ctf_entry.grid(row=0, column=1)


def create_table():
    table_name = ctf_entry.get()
    global table_create_success
    global db
    try:
        db = DB()
        db.conn.execute(f""" CREATE TABLE {table_name} (
        barcode text NOT NULL PRIMARY KEY,
        length integer NOT NULL,
        width integer NOT NULL,
        height integer NOT NULL,
        level integer NOT NULL); """)
        ctf_entry.delete(0, END)
        table_create_success.destroy()
        table_create_success = Label(create_frame, text=f"Racking {table_name} created successfully", fg="#0ea600")
        table_create_success.grid(row=2, column=0, columnspan=2)
    except sqlite3.OperationalError:
        messagebox.showwarning("Ops", "Please enter a valid name."
                                      "The name might be used for other racking.")
    db.conn.commit()
    db.conn.close()


ctf_button = Button(create_frame, text="Create", command=create_table)
ctf_button.grid(row=1, column=0)


def check_table():
    global db
    ct_root = Tk()
    ct_root.title("Created racking")
    ct_root.geometry('300x600')
    db = DB()
    db.cursor.execute(""" SELECT name FROM sqlite_master WHERE type = 'table' """)
    results = db.cursor.fetchall()
    i = 0
    for result in results:
        temp_index = Label(ct_root, text=f"{i+1}.  ")
        temp_index.grid(row=i, column=0)
        temp_label = Label(ct_root, text=result)
        temp_label.grid(row=i, column=1)
        i += 1

    ct_root.mainloop()


check_racking_button = Button(create_frame, text="Check racking", command=check_table)
check_racking_button.grid(row=1, column=1)

table_create_success = Label(create_frame, text="")
table_create_success.grid(row=2, column=0, columnspan=2)
########################################################################################################################
# Insert items to table
########################################################################################################################
insert_frame = LabelFrame(root, text="Insert product into a racking", padx=10, pady=10)
insert_frame.grid(row=1, column=0)

racking_name_label = Label(insert_frame, text="Racking name : ", padx=5, pady=5)
racking_name_label.grid(row=0, column=0)
racking_name_entry = Entry(insert_frame)
racking_name_entry.grid(row=0, column=1)

barcode_label = Label(insert_frame, text="Product barcode : ", padx=5, pady=5)
barcode_label.grid(row=1, column=0)
barcode_entry = Entry(insert_frame)
barcode_entry.grid(row=1, column=1)

length_label = Label(insert_frame, text="Length : ", padx=5, pady=5)
length_label.grid(row=2, column=0)
length_entry = Entry(insert_frame)
length_entry.grid(row=2, column=1)

width_label = Label(insert_frame, text="Width : ", padx=5, pady=5)
width_label.grid(row=3, column=0)
width_entry = Entry(insert_frame)
width_entry.grid(row=3, column=1)

height_label = Label(insert_frame, text="Height : ", padx=5, pady=5)
height_label.grid(row=4, column=0)
height_entry = Entry(insert_frame)
height_entry.grid(row=4, column=1)

level_label = Label(insert_frame, text="Level : ", padx=5, pady=5)
level_label.grid(row=5, column=0)
level_entry = Entry(insert_frame)
level_entry.grid(row=5, column=1)


def insert_product():
    global insert_product_success
    racking_name = racking_name_entry.get()
    barcode = barcode_entry.get()
    length = length_entry.get()
    width = width_entry.get()
    height = height_entry.get()
    level = level_entry.get()
    global db
    try:
        db = DB()
        db.conn.execute(f""" INSERT INTO {racking_name} VALUES ({barcode}, {length}, {width}, {height}, {level}) """)
        barcode_entry.delete(0, END)
        length_entry.delete(0, END)
        width_entry.delete(0, END)
        height_entry.delete(0, END)
        level_entry.delete(0, END)
        insert_product_success.destroy()
        insert_product_success = Label(insert_frame, text=f"Product {barcode} inserted successfully",
                                       fg="#0ea600")
        insert_product_success.grid(row=7, column=0, columnspan=2)
    except sqlite3.OperationalError:
        messagebox.showwarning("Ops", "Please enter valid product information."
                                      "Create the racking if it does not exist.")
    except sqlite3.IntegrityError:
        messagebox.showwarning("Ops", "Please make sure the barcode is unique.")
    db.conn.commit()
    db.conn.close()


ipf_button = Button(insert_frame, text="Insert", width=30, command=insert_product)
ipf_button.grid(row=6, column=0, columnspan=2)

insert_product_success = Label(insert_frame, text="")
insert_product_success.grid(row=7, column=0, columnspan=2)
########################################################################################################################
# Query product from table
########################################################################################################################
query_frame = LabelFrame(root, text="Display racking or search product", padx=10, pady=10)
query_frame.grid(row=2, column=0)

table_label = Label(query_frame, text="Racking name : ", padx=5, pady=5)
table_label.grid(row=0, column=0)
table_entry = Entry(query_frame)
table_entry.grid(row=0, column=1)

product_label = Label(query_frame, text="Product barcode : ", padx=5, pady=5)
product_label.grid(row=1, column=0)
product_entry = Entry(query_frame)
product_entry.grid(row=1, column=1)


def display_table():
    table = table_entry.get()
    global db
    global query_message
    global output
    global scrollbar
    output.forget()
    try:
        db = DB()
        temp = db.conn.execute(f""" SELECT * FROM {table} ORDER BY level """)
        query = temp.fetchall()
        result = BeautifulTable()
        for item in query:
            result.rows.append(item)
        result.columns.header = ("Barcode", "Length", "Width", "Height", "Level")
        scrollbar = Scrollbar(root)
        scrollbar.grid(row=0, column=2, rowspan=5, sticky=N + S)
        output = Text(root, height=46)
        output.insert(INSERT, result)
        output.grid(row=0, column=1, rowspan=5)
        output.config(yscrollcommand=scrollbar.set, state=DISABLED)
        scrollbar.config(command=output.yview)
        query_message.destroy()
        query_message = Label(query_frame, text=f"Successfully query racking {table}", fg="#0ea600")
        query_message.grid(row=3, column=0, columnspan=2)
    except sqlite3.OperationalError:
        messagebox.showwarning("Ops", "Please enter valid racking name.")


dr_button = Button(query_frame, text="Display racking", command=display_table)
dr_button.grid(row=2, column=0)


def search_product():
    table = table_entry.get()
    barcode = product_entry.get()
    global db
    global query_message
    global output
    global scrollbar
    output.forget()
    try:
        db = DB()
        temp = db.conn.execute(f""" SELECT * FROM {table} WHERE barcode = {barcode} """)
        query = temp.fetchall()
        result = BeautifulTable()
        for item in query:
            result.rows.append(item)
        result.columns.header = ("Barcode", "Length", "Width", "Height", "Level")
        scrollbar = Scrollbar(root)
        scrollbar.grid(row=0, column=2, rowspan=5, sticky=N + S)
        output = Text(root, height=46)
        output.insert(INSERT, result)
        output.grid(row=0, column=1, rowspan=5)
        output.config(yscrollcommand=scrollbar.set, state=DISABLED)
        scrollbar.config(command=output.yview)
        query_message.destroy()
        query_message = Label(query_frame, text=f"Successfully search product at racking {table}", fg="#0ea600")
        query_message.grid(row=3, column=0, columnspan=2)
    except sqlite3.OperationalError:
        messagebox.showwarning("Ops", "Please enter valid racking name and product barcode.")


sp_button = Button(query_frame, text="Search product", command=search_product)
sp_button.grid(row=2, column=1)

query_message = Label(query_frame, text="")
query_message.grid(row=3, column=0, columnspan=2)
########################################################################################################################
# Display query output
########################################################################################################################
scrollbar = Scrollbar(root)
scrollbar.grid(row=0, column=2, rowspan=5, sticky=N + S)
output = Text(root, height=46, state=DISABLED)
output.grid(row=0, column=1, rowspan=5, columnspan=1)
output.insert(INSERT, "")
########################################################################################################################
# Delete products or racking
########################################################################################################################
delete_frame = LabelFrame(root, text="Delete product or racking", padx=10, pady=10)
delete_frame.grid(row=3, column=0)

dpf_racking_label = Label(delete_frame, text="Racking name : ", padx=5, pady=5)
dpf_racking_label.grid(row=0, column=0)
dpf_racking_entry = Entry(delete_frame)
dpf_racking_entry.grid(row=0, column=1)

dpf_barcode_label = Label(delete_frame, text="Barcode : ", padx=5, pady=5)
dpf_barcode_label.grid(row=1, column=0)
dpf_barcode_entry = Entry(delete_frame)
dpf_barcode_entry.grid(row=1, column=1)


def delete_product():
    racking = dpf_racking_entry.get()
    barcode = dpf_barcode_entry.get()
    global db
    global delete_success
    try:
        dpf_racking_entry.delete(0, END)
        dpf_barcode_entry.delete(0, END)
        db = DB()
        db.conn.execute(f""" DELETE FROM {racking} WHERE barcode = {barcode} """)
        delete_success.destroy()
        delete_success = Label(delete_frame, text=f"Successfully delete {barcode} from {racking}", fg="#0ea600")
        delete_success.grid(row=3, column=0, columnspan=2)
    except sqlite3.OperationalError:
        messagebox.showwarning("Ops", "Please enter valid racking name and product barcode.")
    db.conn.commit()
    db.conn.close()


def remove_racking():
    racking = dpf_racking_entry.get()
    global db
    global delete_success
    try:
        dpf_racking_entry.delete(0, END)
        dpf_barcode_entry.delete(0, END)
        db = DB()
        db.conn.execute(f""" DROP TABLE {racking} """)
        delete_success.destroy()
        delete_success = Label(delete_frame, text=f"Successfully remove racking {racking}", fg="#0ea600")
        delete_success.grid(row=3, column=0, columnspan=2)
    except sqlite3.OperationalError:
        messagebox.showwarning("Ops", "Please make sure you enter the racking name that you want to delete, "
                                      "or the racking does not exist.")
    db.conn.commit()
    db.conn.close()


delete_product_button = Button(delete_frame, text="Delete product", command=delete_product)
delete_product_button.grid(row=2, column=0)

delete_table_button = Button(delete_frame, text="Remove racking", command=remove_racking)
delete_table_button.grid(row=2, column=1)

delete_success = Label(delete_frame, text="")
delete_success.grid(row=3, column=0, columnspan=2)
########################################################################################################################
# Update product or racking
########################################################################################################################
update_frame = LabelFrame(root, text="Update product or rename racking", padx=10, pady=10)
update_frame.grid(row=4, column=0)


def update_product_tk():
    up_root = Tk()
    up_root.title("Update product")
    up_root.iconbitmap(icon)

    original_frame = LabelFrame(up_root, text="Set product at", padx=10, pady=10)
    original_frame.grid(row=0, column=0)

    of_racking_label = Label(original_frame, text="Racking : ", padx=5, pady=5)
    of_racking_label.grid(row=0, column=0)
    of_racking_entry = Entry(original_frame)
    of_racking_entry.grid(row=0, column=1)

    of_barcode_label = Label(original_frame, text="Barcode : ", padx=5, pady=5)
    of_barcode_label.grid(row=1, column=0)
    of_barcode_entry = Entry(original_frame)
    of_barcode_entry.grid(row=1, column=1)

    new_frame = LabelFrame(up_root, text="To", padx=10, pady=10)
    new_frame.grid(row=1, column=0)

    n_barcode_label = Label(new_frame, text="Barcode : ", padx=5, pady=5)
    n_barcode_label.grid(row=0, column=0)
    n_barcode_entry = Entry(new_frame)
    n_barcode_entry.grid(row=0, column=1)

    n_length_label = Label(new_frame, text="Length : ", padx=5, pady=5)
    n_length_label.grid(row=1, column=0)
    n_length_entry = Entry(new_frame)
    n_length_entry.grid(row=1, column=1)

    n_width_label = Label(new_frame, text="Width : ", padx=5, pady=5)
    n_width_label.grid(row=2, column=0)
    n_width_entry = Entry(new_frame)
    n_width_entry.grid(row=2, column=1)

    n_height_label = Label(new_frame, text="Height : ", padx=5, pady=5)
    n_height_label.grid(row=3, column=0)
    n_height_entry = Entry(new_frame)
    n_height_entry.grid(row=3, column=1)

    n_level_label = Label(new_frame, text="Level : ", padx=5, pady=5)
    n_level_label.grid(row=4, column=0)
    n_level_entry = Entry(new_frame)
    n_level_entry.grid(row=4, column=1)

    def update_product():
        global update_success
        racking = of_racking_entry.get()
        old_bar = of_barcode_entry.get()
        barcode = n_barcode_entry.get()
        length = n_length_entry.get()
        width = n_width_entry.get()
        height = n_height_entry.get()
        level = n_level_entry.get()
        global db
        try:
            db.conn.execute(f""" UPDATE {racking} 
            SET barcode = {barcode},
                length = {length},
                width = {width},
                height = {height},
                level = {level}
            WHERE barcode = {old_bar} """)
            messagebox.showinfo("Wow", "Product information has successfully updated.")
            update_success.destroy()
            update_success = Label(update_frame, text="Successfully updated", fg="#0ea600")
            update_success.grid(row=1, column=0, columnspan=2)
        except sqlite3.OperationalError:
            messagebox.showwarning("Ops", "Please enter valid product information.")
        db.conn.commit()
        db.conn.close()
        up_root.destroy()

    update_button = Button(up_root, text="Update", command=update_product)
    update_button.grid(row=1, column=2, sticky=S)

    up_root.mainloop()


update_product_button = Button(update_frame, text="Update product", command=update_product_tk)
update_product_button.grid(row=0, column=0)


def rename_racking_tk():
    rr_root = Tk()
    rr_root.title("Rename racking")
    rr_root.geometry('300x100')
    rr_root.iconbitmap(icon)

    old_racking_label = Label(rr_root, text="Original name : ", padx=5, pady=5)
    old_racking_label.grid(row=0, column=0)
    old_racking_entry = Entry(rr_root)
    old_racking_entry.grid(row=0, column=1)

    new_racing_label = Label(rr_root, text="New name : ", padx=5, pady=5)
    new_racing_label.grid(row=1, column=0)
    new_racing_entry = Entry(rr_root)
    new_racing_entry.grid(row=1, column=1)

    def rename_table():
        global update_success
        old = old_racking_entry.get()
        new = new_racing_entry.get()
        global db
        try:
            db = DB()
            db.conn.execute(f""" ALTER TABLE {old} RENAME TO {new}; """)
            messagebox.showinfo("Wow", f"Racking name changed from {old} to {new}.")
            update_success.destroy()
            update_success = Label(update_frame, text="Successfully rename", fg="#0ea600")
            update_success.grid(row=1, column=0, columnspan=2)
        except sqlite3.OperationalError:
            messagebox.showwarning("Ops", "Please make sure the table is exist and the name must be unique.")
        db.conn.commit()
        db.conn.close()
        rr_root.destroy()

    rename_button = Button(rr_root, text="Rename", command=rename_table)
    rename_button.grid(row=2, column=2)

    rr_root.mainloop()


rename_racking_button = Button(update_frame, text="Rename racking", command=rename_racking_tk)
rename_racking_button.grid(row=0, column=1)

update_success = Label(update_frame, text="")
update_success.grid(row=1, column=0, columnspan=2)
########################################################################################################################
root.mainloop()
