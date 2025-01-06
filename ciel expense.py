import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import sqlite3
from tkcalendar import Calendar

# Initialize the Tkinter Application
root = tk.Tk()
root.title("Expense Tracker")
root.configure(bg="#FFB7c5")

expense_list_frame = ttk.Frame(root, padding=(10, 10))
expense_list_frame.grid(row=1, column=0, columnspan=20, padx=20, pady=20, sticky="nsew")

# Create a frame for the data entry section
data_entry_frame = ttk.Frame(root)
data_entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a frame for buttons
button_frame = ttk.Frame(data_entry_frame)
button_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="w")

# Define fonts and colors
btn_font = ('system', 14)

# Create StringVars for entry fields
date = tk.StringVar()
payee = tk.StringVar()
desc = tk.StringVar()
amnt = tk.DoubleVar()
MoP = tk.StringVar()

# Create GUI elements
# Create GUI elements
date_label = ttk.Label(data_entry_frame, text="Date:", background="#FFB7c5")
date_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="e")  # Adjust padx and sticky

date_entry = ttk.Entry(data_entry_frame, textvariable=date, background="#FFB7c5")
date_entry.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="w")  # Adjust padx and sticky

payee_label = ttk.Label(data_entry_frame, text="Payee:", background="#FFB7c5")
payee_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="e")  # Adjust padx and sticky

payee_entry = ttk.Entry(data_entry_frame, textvariable=payee, background="#FFB7c5")
payee_entry.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="w")  # Adjust padx and sticky

desc_label = ttk.Label(data_entry_frame, text="Description:", background="#FFB7c5")
desc_label.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="e")  # Adjust padx and sticky

desc_entry = ttk.Entry(data_entry_frame, textvariable=desc, background="#FFB7c5")
desc_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="w")  # Adjust padx and sticky

amnt_label = ttk.Label(data_entry_frame, text="Amount:", background="#FFB7c5")
amnt_label.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="e")  # Adjust padx and sticky

amnt_entry = ttk.Entry(data_entry_frame, textvariable=amnt, background="#FFB7c5")
amnt_entry.grid(row=3, column=1, padx=(5, 10), pady=5, sticky="w")  # Adjust padx and sticky

MoP_label = ttk.Label(data_entry_frame, text="Mode of Payment:", background="#FFB7c5")
MoP_label.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="e")  # Adjust padx and sticky

MoP_entry = ttk.Entry(data_entry_frame, textvariable=MoP, background="#FFB7c5")
MoP_entry.grid(row=4, column=1, padx=(5, 10), pady=5, sticky="w")  # Adjust padx and sticky


# Style configuration for buttons and entry fields
style = ttk.Style()
style.configure('TButton', background='#90e0ef')
style.configure('TEntry', fieldbackground='#FFB7c5')

# Create a frame for the expense list
expense_list_frame = ttk.Frame(root)
expense_list_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Create a Treeview for displaying expenses with specific columns
table = ttk.Treeview(
    expense_list_frame,
    columns=("ID", "Date", "Payee", "Amount", "ModeOfPayment"),
    show="headings",
    height=15  # Adjust the height as needed
)

# Define column headings
table.heading("ID", text="ID")
table.heading("Date", text="Date")
table.heading("Payee", text="Payee")
table.heading("Amount", text="Amount")
table.heading("ModeOfPayment", text="Mode of Payment")

# Adjust the column widths
table.column("ID", width=50)
table.column("Date", width=100)
table.column("Payee", width=150)
table.column("Amount", width=100)
table.column("ModeOfPayment", width=120)

table.pack(fill=tk.BOTH, expand=True)  # Expand the table to fill available space

# Initialize SQLite connection and cursor
connector = sqlite3.connect('expense_database.db')
connector.execute('CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT, Date DATE, Payee TEXT, Description TEXT, Amount REAL, ModeOfPayment TEXT)')
connector.commit()

# Functions (remaining functions are unchanged)
# ...

# Create buttons in a button group (remaining buttons are unchanged)
# ...

# Functions
def add_another_expense():
    # Function to add a new expense to the database
    try:
        date_value = date.get()
        payee_value = payee.get()
        desc_value = desc.get()
        amnt_value = amnt.get()
        MoP_value = MoP.get()

        if not date_value or not payee_value or not desc_value or not amnt_value or not MoP_value:
            mb.showerror('Incomplete Information', 'Please fill in all the fields.')
            return

        connector.execute(
            'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
            (date_value, payee_value, desc_value, amnt_value, MoP_value)
        )
        connector.commit()

        clear_fields()
        list_all_expenses()
        mb.showinfo('Expense Added', 'The expense has been successfully added.')

    except Exception as e:
        mb.showerror('Error', str(e))

def edit_expense():
    # Function to edit an existing expense in the database
    try:
        if not table.selection():
            mb.showerror('No Expense Selected', 'Please select an expense from the list to edit.')
            return

        date_value = date.get()
        payee_value = payee.get()
        desc_value = desc.get()
        amnt_value = amnt.get()
        MoP_value = MoP.get()

        if not date_value or not payee_value or not desc_value or not amnt_value or not MoP_value:
            mb.showerror('Incomplete Information', 'Please fill in all the fields.')
            return

        current_selected_expense = table.item(table.focus())
        expense_id = current_selected_expense['values'][0]

        connector.execute(
            'UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
            (date_value, payee_value, desc_value, amnt_value, MoP_value, expense_id)
        )
        connector.commit()

        clear_fields()
        list_all_expenses()
        mb.showinfo('Expense Updated', 'The expense has been successfully updated.')

    except Exception as e:
        mb.showerror('Error', str(e))

def remove_expense():
    # Function to remove an expense from the database
    try:
        if not table.selection():
            mb.showerror('No Expense Selected', 'Please select an expense from the list to remove.')
            return

        current_selected_expense = table.item(table.focus())
        expense_id = current_selected_expense['values'][0]

        surety = mb.askyesno('Confirm Deletion', 'Are you sure you want to delete this expense?')

        if surety:
            connector.execute('DELETE FROM ExpenseTracker WHERE ID = ?', (expense_id,))
            connector.commit()

            list_all_expenses()
            mb.showinfo('Expense Removed', 'The expense has been successfully removed.')

    except Exception as e:
        mb.showerror('Error', str(e))

def clear_fields():
    # Function to clear entry fields
    date.set('')
    payee.set('')
    desc.set('')
    amnt.set('')
    MoP.set('')

def view_expense_details():
    # Function to view details of a selected expense
    if not table.selection():
        mb.showerror('No Expense Selected', 'Please select an expense from the list to view details.')
        return

    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']

    date.set(values[1])
    payee.set(values[2])
    desc.set(values[3])
    amnt.set(values[4])
    MoP.set(values[5])

def list_all_expenses():
    # Function to list all expenses from the database in the Treeview
    table.delete(*table.get_children())

    all_data = connector.execute('SELECT * FROM ExpenseTracker')
    data = all_data.fetchall()

    for values in data:
        table.insert('', tk.END, values=values)

def selected_expense_to_words():
    # Function to convert details of the selected expense to words
    if not table.selection():
        mb.showerror('No Expense Selected', 'Please select an expense from the list to convert to words.')
        return

    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']

    message = f'Your expense can be read like: ' \
              f'\n"You paid {values[4]} to {values[2]} for {values[3]} on {values[1]} via {values[5]}"'

    mb.showinfo('Expense in Words', message)

# Create buttons in a button group
add_button = tk.Button(button_frame, text="Add Expense", command=add_another_expense, background='#90e0ef', font=btn_font)
edit_button = tk.Button(button_frame, text="Edit Expense", command=edit_expense, background='#90e0ef', font=btn_font)
remove_button = tk.Button(button_frame, text="Remove Expense", command=remove_expense, background='#90e0ef', font=btn_font)
clear_button = tk.Button(button_frame, text="Clear Fields", command=clear_fields, background='#90e0ef', font=btn_font)
view_button = tk.Button(button_frame, text="View Expense Details", command=view_expense_details, background='#90e0ef', font=btn_font)
list_all_button = tk.Button(button_frame, text="List All Expenses", command=list_all_expenses, background='#90e0ef', font=btn_font)
read_button = tk.Button(button_frame, text="Read Expense Details", command=selected_expense_to_words, background='#90e0ef', font=btn_font)

add_button.grid(row=0, column=0, padx=5)
edit_button.grid(row=0, column=1, padx=5)
remove_button.grid(row=0, column=2, padx=5)
clear_button.grid(row=1, column=0, padx=5)
view_button.grid(row=1, column=1, padx=5)
list_all_button.grid(row=1, column=2, padx=5)
read_button.grid(row=2, column=0, padx=5, columnspan=3)

cal = Calendar(data_entry_frame, font=('system', 14), date_pattern='mm/dd/yyyy')
cal.grid(row=0, column=3, rowspan=5, padx=15, pady=15, sticky="nsew")

style.configure('TFrame', background='#FFB7c5')

root.mainloop()
