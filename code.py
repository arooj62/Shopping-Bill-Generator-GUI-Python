# ---------------------------------------------------------
# SHOPPING BILL GENERATOR - PROFESSIONAL EDITION (Tkinter GUI)
# Concepts covered: print(), data types, comments, variables,
# keywords, user input, literals, operators, type conversion,
# while loop, for loop, break, continue, pass
# ---------------------------------------------------------

import tkinter as tk                      # GUI library
from tkinter import ttk, messagebox       # ttk gives us the Combobox (dropdown)
from datetime import datetime             # for invoice date & time

# ---------------- Shop & Global Variables (Literals) ----------------
shop_name = "PyMart Superstore"           # string literal
shop_address = "123 Market Road, Islamabad"
shop_phone = "+92-51-1234567"
tax_rate = 0.05                           # float literal (5% tax)
bill_number = 1000                        # int literal, increased using while loop
cart = []                                 # empty list (data type: list)

# Dictionary of available items -> price (data types: dict, str, float)
menu = {
    "rice": 340.0,
    "wheat": 450.0,
    "sugar": 470.5,
    "milk": 248.0,
    "oil": 420.0,
    "soap": 80.0
}


# ---------------- Keyword & Function Demo ----------------
def is_valid_item(name):
    # 'in' and 'return' are keywords
    if name in menu:
        return True
    else:
        return False


def generate_bill_number():
    # while loop demo: keep increasing until divisible by 3
    global bill_number
    n = bill_number
    while True:
        n += 1
        if n % 3 == 0:          # operator: modulus
            break                # break statement -> stop loop
        else:
            continue              # continue statement -> go to next iteration
    bill_number = n
    return bill_number


def peek_next_bill_number():
    # shows what the NEXT invoice number will be, without changing the real one
    n = bill_number
    while True:
        n += 1
        if n % 3 == 0:
            break
        else:
            continue
    return n


# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title(shop_name + " - Billing System")
root.geometry("460x620")
root.configure(bg="#f2f2f2")

tk.Label(root, text=shop_name, font=("Arial", 18, "bold"), bg="#f2f2f2").pack(pady=(10, 0))
tk.Label(root, text=shop_address, font=("Arial", 9), bg="#f2f2f2").pack()
tk.Label(root, text="Ph: " + shop_phone, font=("Arial", 9), bg="#f2f2f2").pack(pady=(0, 5))

invoice_no_label = tk.Label(root, text=f"Invoice No: {peek_next_bill_number()}",
                             font=("Arial", 10, "bold"), fg="#2196F3", bg="#f2f2f2")
invoice_no_label.pack(pady=(0, 10))

# ---------------- Customer Details Frame ----------------
cust_frame = tk.LabelFrame(root, text="Customer Details", bg="#f2f2f2", padx=10, pady=10)
cust_frame.pack(padx=15, pady=5, fill="x")

tk.Label(cust_frame, text="Name:", bg="#f2f2f2").grid(row=0, column=0, sticky="w", pady=3)
customer_name_entry = tk.Entry(cust_frame, width=25)          # taking user input via GUI
customer_name_entry.grid(row=0, column=1, pady=3)

tk.Label(cust_frame, text="Phone:", bg="#f2f2f2").grid(row=1, column=0, sticky="w", pady=3)
customer_phone_entry = tk.Entry(cust_frame, width=25)         # taking user input via GUI
customer_phone_entry.grid(row=1, column=1, pady=3)

# ---------------- Item Entry Frame ----------------
item_frame = tk.LabelFrame(root, text="Add Item", bg="#f2f2f2", padx=10, pady=10)
item_frame.pack(padx=15, pady=5, fill="x")

tk.Label(item_frame, text="Item Name:", bg="#f2f2f2").grid(row=0, column=0, sticky="w", pady=3)

# Combobox lets the customer SELECT an item instead of typing it
item_names = list(menu.keys())                    # convert dict keys to a list (data type demo)
item_combo = ttk.Combobox(item_frame, width=18, values=item_names, state="readonly")
item_combo.grid(row=0, column=1, pady=3)
item_combo.current(0)                              # select the first item by default

price_label = tk.Label(item_frame, text=f"Price: Rs {menu[item_names[0]]:.2f}", bg="#f2f2f2", fg="gray")
price_label.grid(row=0, column=2, padx=(10, 0))


def on_item_selected(event):
    # updates the price preview whenever a different item is picked
    selected = item_combo.get()
    price_label.config(text=f"Price: Rs {menu[selected]:.2f}")


item_combo.bind("<<ComboboxSelected>>", on_item_selected)   # keyword: event binding

tk.Label(item_frame, text="Quantity:", bg="#f2f2f2").grid(row=1, column=0, sticky="w", pady=3)
qty_entry = tk.Entry(item_frame, width=20)
qty_entry.grid(row=1, column=1, pady=3)

cart_box = tk.Listbox(root, width=55, height=10, font=("Consolas", 10))
cart_box.pack(pady=10)

total_label = tk.Label(root, text="Total: Rs 0.00", font=("Arial", 13, "bold"), bg="#f2f2f2")
total_label.pack(pady=5)


# ---------------- Core Logic ----------------
def add_item():
    name = item_combo.get().lower().strip()   # get the SELECTED item from dropdown
    qty_str = qty_entry.get().strip()

    if name == "":
        pass   # pass statement: placeholder, dropdown always has a value once items exist

    if not is_valid_item(name):
        messagebox.showerror("Invalid Item", f'"{name}" is not available in the menu!')
        return

    try:
        qty = int(qty_str)          # type conversion: str -> int
    except ValueError:
        messagebox.showerror("Invalid Quantity", "Please enter a valid whole number!")
        return

    if qty <= 0:
        messagebox.showerror("Invalid Quantity", "Quantity must be greater than zero!")
        return

    price = menu[name]              # float value from dict
    subtotal = price * qty          # arithmetic operator

    # for loop demo: check if item already exists in cart, update it
    found = False
    for entry in cart:
        if entry["name"] == name:
            entry["qty"] += qty
            entry["subtotal"] = entry["qty"] * price
            found = True
            break                   # break once found
        else:
            continue                # continue searching

    if not found:
        cart.append({"name": name, "qty": qty, "price": price, "subtotal": subtotal})

    refresh_cart()
    qty_entry.delete(0, tk.END)


def remove_selected_item():
    selection = cart_box.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select an item to remove!")
        return

    index = selection[0]
    # for loop with break to remove the exact matching entry
    for i, entry in enumerate(cart):
        if i == index:
            cart.pop(i)
            break
        else:
            continue

    refresh_cart()


def refresh_cart():
    cart_box.delete(0, tk.END)
    total = 0.0
    for entry in cart:                       # for loop over cart list
        line = f'{entry["name"].title():<10}x{entry["qty"]:<4} Rs {entry["subtotal"]:.2f}'
        cart_box.insert(tk.END, line)
        total += entry["subtotal"]           # operator: +=

    tax_amount = total * tax_rate            # operator: *
    grand_total = total + tax_amount         # operator: +
    total_label.config(text=f"Total: Rs {grand_total:.2f} (incl. tax)")


def generate_final_bill():
    customer_name = customer_name_entry.get().strip()
    customer_phone = customer_phone_entry.get().strip()

    if customer_name == "":
        messagebox.showerror("Missing Info", "Please enter the customer's name!")
        return

    if len(cart) == 0:
        messagebox.showwarning("Empty Cart", "Add items before generating the bill!")
        return

    bno = generate_bill_number()
    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")   # current date & time

    receipt_lines = []                        # list to store receipt text
    receipt_lines.append("=" * 42)
    receipt_lines.append(shop_name.center(42))
    receipt_lines.append(shop_address.center(42))
    receipt_lines.append(("Ph: " + shop_phone).center(42))
    receipt_lines.append("=" * 42)
    receipt_lines.append(f"Invoice No : {bno}")
    receipt_lines.append(f"Date & Time: {now}")
    receipt_lines.append(f"Customer   : {customer_name}")
    receipt_lines.append(f"Phone      : {customer_phone if customer_phone else 'N/A'}")
    receipt_lines.append("-" * 42)
    receipt_lines.append(f'{"Item":<12}{"Qty":<6}{"Price":<10}{"Amount":<10}')
    receipt_lines.append("-" * 42)

    total = 0.0
    for entry in cart:                        # for loop to build item rows
        row = f'{entry["name"].title():<12}{entry["qty"]:<6}{entry["price"]:<10.2f}{entry["subtotal"]:<10.2f}'
        receipt_lines.append(row)
        total += entry["subtotal"]

    tax_amount = total * tax_rate
    grand_total = total + tax_amount
    receipt_lines.append("-" * 42)
    receipt_lines.append(f'{"Subtotal:":<32}Rs {total:.2f}')
    receipt_lines.append(f'{"Tax (5%):":<32}Rs {tax_amount:.2f}')
    receipt_lines.append(f'{"Grand Total:":<32}Rs {grand_total:.2f}')
    receipt_lines.append("=" * 42)
    receipt_lines.append("Thank you for shopping with us!".center(42))
    receipt_lines.append("=" * 42)

    # print() the full receipt to console
    for line in receipt_lines:
        print(line)

    # save receipt to a text file for record-keeping
    filename = f"invoice_{bno}.txt"
    with open(filename, "w") as file:
        for line in receipt_lines:
            file.write(line + "\n")

    messagebox.showinfo(
        "Bill Generated",
        f"Invoice No: {bno}\nCustomer: {customer_name}\nGrand Total: Rs {grand_total:.2f}\n\nSaved as {filename}"
    )

    cart.clear()
    refresh_cart()
    customer_name_entry.delete(0, tk.END)
    customer_phone_entry.delete(0, tk.END)
    invoice_no_label.config(text=f"Invoice No: {peek_next_bill_number()}")


# ---------------- Buttons ----------------
btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Item", command=add_item, width=14, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Remove Selected", command=remove_selected_item, width=14, bg="#f44336", fg="white").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Generate Bill", command=generate_final_bill, width=14, bg="#2196F3", fg="white").grid(row=0, column=2, padx=5)

tk.Label(root, text="Select an item from the dropdown, set quantity, then click Add Item", fg="gray", bg="#f2f2f2").pack(pady=5)

root.mainloop()