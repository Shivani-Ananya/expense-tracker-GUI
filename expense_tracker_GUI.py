import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import json

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("900x800")

label = tk.Label(root, text = "Welcome to the Expense Tracker", font = ("Aerial", 14))
label.pack()

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(pady=20)

def add_expense():
    add_window = tk.Toplevel(root)
    add_window.title("Add New Expense")
    add_window.geometry("400x400")
    title_label = tk.Label(add_window, text="Add New Expense", font=("Arial", 16))
    title_label.pack(pady=20)
    date_label = tk.Label(add_window, text="Date (YYYY-MM-DD):", font=("Arial", 12))
    date_label.pack()
    date_entry = tk.Entry(add_window, font=("Arial", 12))
    date_entry.pack(pady=5)
    date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
    category_label = tk.Label(add_window, text="Category:", font=("Arial", 12))
    category_label.pack()
    category_entry = tk.Entry(add_window, font=("Arial", 12))
    category_entry.pack(pady=5)
    amount_label = tk.Label(add_window, text="Amount (₹):", font=("Arial", 12))
    amount_label.pack()
    amount_entry = tk.Entry(add_window, font=("Arial", 12))
    amount_entry.pack(pady=5)
    def save_expense():
        date = date_entry.get()
        category = category_entry.get()
        amount = amount_entry.get()
        if date == "" or category == "" or amount == "":
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return
        new_expense = {"date": date, "category": category, "amount": amount}
        try:
            with open("expenses.json", "r") as file:
                expenses = json.load(file)
        except FileNotFoundError:
            expenses = []
        expenses.append(new_expense)
        with open("expenses.json", "w") as file:
            json.dump(expenses, file, indent=4)
        messagebox.showinfo("Success", "Expense added successfully!")
        add_window.destroy()
    add_button = tk.Button(add_window, text="Add Expense", font=("Arial", 12), bg="#CC66DA", fg="black", command=save_expense)
    add_button.pack(pady=10)
    cancel_button = tk.Button(add_window, text="Cancel", font=("Arial", 12), bg="red", fg="white", command=add_window.destroy)
    cancel_button.pack(pady=5)
button1 = tk.Button(frame, text = "Add Expenses", font = ("Serif", 14),  bg="#FDFFB8", fg="black", width=20, command = add_expense)
button1.pack(pady = 20)

def view_expense():
    view_window = tk.Toplevel(root)
    view_window.title("View Expense")
    view_window.geometry("400x400")
    title_label = tk.Label(view_window, text="View Expense", font=("Arial", 16))
    title_label.pack(pady=20)
    columns = ("ID", "Date", "Category", "Amount")
    tree = ttk.Treeview(view_window, columns = columns, show = "headings")
    tree.pack(side="left", fill="both", expand=True, pady=20)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    scrollbar = ttk.Scrollbar(view_window, orient = "vertical", command = tree.yview)
    scrollbar.pack(side = "right", fill = "y")
    tree.configure(yscrollcommand=scrollbar.set)
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []
    for idx, exp in enumerate(expenses, start=1):
        tree.insert("", "end", values=(idx, exp["date"], exp["category"], exp["amount"]))
    close_button = tk.Button(view_window, text="Close", font=("Arial", 12), bg="red", fg="white", command=view_window.destroy)
    close_button.pack(pady=5)
button2 = tk.Button(frame, text = "View expenses", font = ("Serif", 14),  bg="#FDFFB8", fg="black", width=20, command = view_expense)
button2.pack(pady = 20)

columns = ("ID", "Date", "Category", "Amount")
def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
def search_expense():
    search_window = tk.Toplevel(root)
    search_window.title("View Expense")
    search_window.geometry("600x450")
    title_label = tk.Label(search_window, text="Search Expense", font=("Arial", 16))
    title_label.pack(pady=20)
    frame_search = tk.Frame(search_window)
    frame_search.pack(pady=10)
    tk.Label(frame_search, text="Enter Search Date (YYYY-MM-DD):", font=('Arial', 12)).pack(side="left")
    search_entry = tk.Entry(frame_search, width=20, font=('Arial', 12))
    search_entry.pack(side="left", padx=10)
    tree = ttk.Treeview(search_window, columns = columns, show = "headings")
    tree.pack(side="left", fill="both", expand=True, pady=20)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    scrollbar = ttk.Scrollbar(search_window, orient = "vertical", command = tree.yview)
    scrollbar.pack(side = "right", fill = "y")
    tree.configure(yscrollcommand=scrollbar.set)
    def fetch_all():
        tree.delete(*tree.get_children())
        expenses = load_expenses()
        for idx, exp in enumerate(expenses, start=1):
            tree.insert("", "end", values=(idx, exp["date"], exp["category"], exp["amount"]))
    def filter_date():
        search_date = search_entry.get().strip()
        if not search_date:
            messagebox.showerror("Error", "Please enter a date to filter!")
            return
        tree.delete(*tree.get_children())
        expenses = load_expenses()
        filtered = [exp for exp in expenses if exp["date"] == search_date]
        if not filtered:
            messagebox.showinfo("No Results", f"No expenses found for date: {search_date}")
            return
        for idx, exp in enumerate(filtered, start=1):
            tree.insert("", "end", values=(idx, exp["date"], exp["category"], exp["amount"]))
    fetch_all()
    btn_frame = tk.Frame(search_window)
    btn_frame.pack(pady=15, fill='x', padx=20)
    btn_frame.update_idletasks()
    btn_frame.config(height=50)
    fetch_button = tk.Button(btn_frame, text="Fetch All Expenses", font=("Arial", 12), bg="#CC66DA", fg="black", command=fetch_all)
    fetch_button.pack(side="left", padx=(0, 10), fill='x', expand=True)
    filter_button = tk.Button(btn_frame, text="Filter by Date", font=("Arial", 12), bg="#CC66DA", fg="black", command=filter_date)
    filter_button.pack(side="left" , padx=(0, 10), fill='x', expand=True)
    close_button = tk.Button(search_window, text="Close", font=("Arial", 12), bg="red", fg="white", command=search_window.destroy)
    close_button.pack(pady=10)
button3 = tk.Button(frame, text = "Search Expenses", font = ("Serif", 14),  bg="#FDFFB8", fg="black", width=20, command = search_expense)
button3.pack(pady = 20)

def delete_expense():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Expense")
    delete_window.geometry("400x400")
    title_label = tk.Label(delete_window, text="Delete Expense", font=("Arial", 16))
    title_label.pack(pady=20)
    tree = ttk.Treeview(delete_window, columns = columns, show = "headings")
    tree.pack(side="left", fill="both", expand=True, pady=20)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    scrollbar = ttk.Scrollbar(delete_window, orient = "vertical", command = tree.yview)
    scrollbar.pack(side = "right", fill = "y")
    tree.configure(yscrollcommand=scrollbar.set)
    expenses = load_expenses()
    for idx, exp in enumerate(expenses, start=1):
        tree.insert("", "end", values=(idx, exp["date"], exp["category"], exp["amount"]))
    def delete_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No expense selected to delete!")
            return
        idx = tree.index(selected_item)
        expenses.pop(idx) 
        with open("expenses.json", "w") as file:
            json.dump(expenses, file, indent=4)
        tree.delete(selected_item)
        messagebox.showinfo("Deleted", "Expense deleted successfully!")
    delete_button = tk.Button(delete_window, text="Delete Selected", font=('Arial', 14), bg="#FE7743", fg="black", width=20, command=delete_selected)
    delete_button.pack(pady=10)
    close_button = tk.Button(delete_window, text="Close", font=("Arial", 12), bg="red", fg="white", command=delete_window.destroy)
    close_button.pack(pady=5)
button4 = tk.Button(frame, text = "Delete Expenses", font = ("Serif", 14),  bg="#FDFFB8", fg="black", width=20, command = delete_expense)
button4.pack(pady = 20)

exit_button =  tk.Button(frame, text="Exit App", command=root.destroy, font=("Arial", 16), bg="red", fg="white")
exit_button.pack(pady = 20)
