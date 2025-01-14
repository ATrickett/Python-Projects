import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta


def initialize_db():
    """Initialize the SQLite database and create the assignments table."""
    conn = sqlite3.connect("assignments.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class TEXT NOT NULL,
            assignment TEXT NOT NULL,
            due_date TEXT NOT NULL,
            notes TEXT,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def fetch_classes():
    """Fetch all distinct classes for the dropdown menu."""
    conn = sqlite3.connect("assignments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT class FROM assignments")
    classes = ["All"] + [row[0] for row in cursor.fetchall()]
    conn.close()
    return classes


def refresh_class_filter(selected_class=None):
    """Refresh the class dropdown menu dynamically, retaining the current filter."""
    classes = fetch_classes()
    current_selection = selected_class if selected_class else class_filter_var.get()
    class_filter_var.set(current_selection)
    class_filter_menu["menu"].delete(0, "end")
    for cls in classes:
        class_filter_menu["menu"].add_command(label=cls, command=lambda value=cls: on_filter_change(value))


def refresh_assignments(selected_class=None, start_date=None, end_date=None):
    """Refresh the assignment list based on the selected filters."""
    if not selected_class:
        selected_class = class_filter_var.get()

    conn = sqlite3.connect("assignments.db")
    cursor = conn.cursor()

    query = "SELECT id, completed, class, assignment, due_date FROM assignments"
    params = []

    # Add class filter
    if selected_class and selected_class != "All":
        query += " WHERE class = ?"
        params.append(selected_class)

    # Add date range filter
    if start_date and end_date:
        if "WHERE" in query:
            query += " AND due_date BETWEEN ? AND ?"
        else:
            query += " WHERE due_date BETWEEN ? AND ?"
        params.append(start_date)
        params.append(end_date)

    query += " ORDER BY due_date"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    # Clear the Treeview
    for row in assignment_tree.get_children():
        assignment_tree.delete(row)

    # Populate the Treeview with rows
    for row in rows:
        completed = "Yes" if row[1] == 1 else "No"
        assignment_tree.insert("", "end", iid=row[0], values=(completed, row[2], row[3], row[4]))


def on_filter_change(selected_class):
    """Handle changes in the class filter dropdown."""
    start_date = start_date_var.get()
    end_date = end_date_var.get()
    refresh_assignments(selected_class, start_date, end_date)


def apply_date_filter():
    """Apply the date filter based on user input."""
    start_date = start_date_var.get()
    end_date = end_date_var.get()
    if not start_date or not end_date:
        messagebox.showerror("Error", "Please select both start and end dates.")
        return

    try:
        datetime.strptime(start_date, "%m-%d-%y")
        datetime.strptime(end_date, "%m-%d-%y")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use MM-DD-YY.")
        return

    refresh_assignments(class_filter_var.get(), start_date, end_date)


def add_assignment():
    """Add a new assignment to the database."""
    class_name = class_var.get()
    assignment_name = assignment_var.get()
    due_date = due_date_var.get()
    notes = notes_var.get()

    if not class_name or not assignment_name or not due_date:
        messagebox.showerror("Error", "Please fill in all required fields!")
        return

    try:
        date_obj = datetime.strptime(due_date, "%m-%d-%y")
        due_date = date_obj.strftime("%m-%d-%y")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use MM-DD-YY.")
        return

    conn = sqlite3.connect("assignments.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO assignments (class, assignment, due_date, notes)
        VALUES (?, ?, ?, ?)
    """, (class_name, assignment_name, due_date, notes))
    conn.commit()
    conn.close()

    current_filter = class_filter_var.get()
    refresh_assignments(current_filter)
    refresh_class_filter(current_filter)
    clear_inputs()


def clear_inputs():
    """Clear the input fields."""
    class_var.set("")
    assignment_var.set("")
    due_date_var.set("")
    notes_var.set("")
    add_button.config(text="Add Assignment", command=add_assignment)


# GUI Setup
root = Tk()
root.title("Assignment Tracker")
root.geometry("900x600")
root.minsize(900, 600)

# Configure grid weights
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)  # Ensure input fields stretch
root.rowconfigure(10, weight=1)  # Allow Treeview row to expand

# Default dates
today = datetime.now()
default_end_date = today + timedelta(days=30)

start_date_var = StringVar()
end_date_var = StringVar(value=default_end_date.strftime("%m-%d-%y"))

# Input Fields
Label(root, text="Class:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
class_var = StringVar()
Entry(root, textvariable=class_var).grid(row=0, column=1, sticky="ew", padx=10, pady=5)

Label(root, text="Assignment:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
assignment_var = StringVar()
Entry(root, textvariable=assignment_var).grid(row=1, column=1, sticky="ew", padx=10, pady=5)

Label(root, text="Due Date (MM-DD-YY):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
due_date_var = StringVar()
DateEntry(root, textvariable=due_date_var, date_pattern="MM-dd-yy", state="normal").grid(row=2, column=1, sticky="ew", padx=10, pady=5)

Label(root, text="Notes:").grid(row=3, column=0, sticky="nw", padx=10, pady=5)
notes_var = StringVar()
Entry(root, textvariable=notes_var).grid(row=3, column=1, sticky="ew", padx=10, pady=5)

# Add Assignment Button
add_button = Button(root, text="Add Assignment", command=add_assignment)
add_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="", ipadx=5, ipady=2)

# Filters
Label(root, text="Filter by Class:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
class_filter_var = StringVar(value="All")
class_filter_menu = OptionMenu(root, class_filter_var, "All", command=on_filter_change)
class_filter_menu.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

Label(root, text="Start Date (MM-DD-YY):").grid(row=6, column=0, sticky="w", padx=10, pady=5)
DateEntry(root, textvariable=start_date_var, date_pattern="MM-dd-yy", state="normal").grid(row=6, column=1, sticky="ew", padx=10, pady=5)

Label(root, text="End Date (MM-DD-YY):").grid(row=7, column=0, sticky="w", padx=10, pady=5)
DateEntry(root, textvariable=end_date_var, date_pattern="MM-dd-yy", state="normal").grid(row=7, column=1, sticky="ew", padx=10, pady=5)

# Apply Date Filter Button
apply_filter_button = Button(root, text="Apply Date Filter", command=apply_date_filter)
apply_filter_button.grid(row=8, column=0, columnspan=2, pady=5, sticky="", ipadx=5, ipady=2)

# Assignment Treeview
Label(root, text="Assignments:").grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=5)
columns = ("Completed", "Class", "Assignment", "Due Date")
assignment_tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
assignment_tree.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Dynamically set column widths
def adjust_treeview_columns():
    treeview_width = assignment_tree.winfo_width()
    ten_percent_width = int(treeview_width * 0.1)
    assignment_tree.column("Completed", width=ten_percent_width, stretch=True)
    assignment_tree.column("Due Date", width=ten_percent_width, stretch=True)
    assignment_tree.column("Class", stretch=True)  # Let this column stretch dynamically
    assignment_tree.column("Assignment", stretch=True)  # Let this column stretch dynamically

# Bind a resize event to dynamically adjust column widths
root.bind("<Configure>", lambda event: adjust_treeview_columns())

# Define Treeview headings
for col in columns:
    assignment_tree.heading(col, text=col)

initialize_db()
refresh_class_filter()
refresh_assignments()

root.mainloop()
