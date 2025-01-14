The **Assignment Tracker** is a Python-based desktop application built with `Tkinter` and `SQLite`. It allows users to manage their assignments, track due dates, and organize tasks by class. Users can add, edit, mark as completed, and delete assignments, as well as filter them by class or date range.

---

## Features

### 1. Add Assignments

- Input assignment details including:
    
    - **Class Name**
        
    - **Assignment Name**
        
    - **Due Date**
        
    - **Notes**
        
- Save assignments to a local SQLite database.
    

### 2. Edit Assignments

- Select an existing assignment from the list to edit.
    
- Update details and save changes back to the database.
    

### 3. Mark as Completed

- Toggle the completion status of an assignment directly from the list.
    

### 4. Delete Assignments

- Permanently delete selected assignments.
    

### 5. Filters

- Filter assignments by:
    
    - **Class** (selectable from a dropdown)
        
    - **Date Range** (start and end dates).
        

### 6. Dynamic Layout

- The assignment display dynamically adjusts column widths based on window size.
    
- Columns for `Completed` and `Due Date` are set to occupy 10% of the display width.
    

---

## Prerequisites

### Python

Make sure you have Python 3.x installed on your system.

### Dependencies

The application requires the following Python libraries:

- `tkinter` (Standard Python GUI library)
    
- `tkcalendar` (Install using `pip install tkcalendar` if not already installed)
    
- `sqlite3` (Comes bundled with Python)
    

---

## Installation

1. **Clone or Download the Repository**
    
    ```
    git clone https://github.com/your-username/assignment-tracker.git
    cd assignment-tracker
    ```
    
2. **Install Dependencies** Make sure you have `tkcalendar` installed:
    
    ```
    pip install tkcalendar
    ```
    
3. **Run the Application** Execute the Python script:
    
    ```
    python Assignment_Tracker.py
    ```
    

---

## Usage

1. **Add Assignments**
    
    - Fill in the required fields (**Class**, **Assignment**, and **Due Date**) and click `Add Assignment`.
        
2. **Edit Assignments**
    
    - Select an assignment from the display list.
        
    - Click `Edit Assignment`, make changes, and save by clicking the `Update Assignment` button.
        
3. **Mark as Completed**
    
    - Select an assignment and click `Mark Completed` to toggle its completion status.
        
4. **Delete Assignments**
    
    - Select an assignment and click `Delete Assignment` to remove it permanently.
        
5. **Filter Assignments**
    
    - Use the dropdown to filter by class.
        
    - Apply date filters by selecting a start and end date, then click `Apply Date Filter`.
        

---

## Screenshots

### Main Interface

### Adding an Assignment

---

## Project Structure

```
assignment-tracker/
│
├── Assignment_Tracker.py   # Main application script
├── assignments.db          # SQLite database (auto-created on first run)
├── README.md               # Project documentation
```

---

## How It Works

- **Database**: The application uses an SQLite database (`assignments.db`) to store assignments. The database is created automatically on the first run.
    
- **GUI**: The graphical user interface is built with `Tkinter`.
    
- **Dynamic Treeview**: Assignments are displayed in a dynamic `Treeview` widget with resizable columns.
    

---

## Future Enhancements

- Add recurring assignments.
    
- Export assignments to CSV or Excel.
    
- Add a search bar for quick filtering.
    
- Add color coding for overdue assignments.
    

---

## Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
    
- [tkcalendar Documentation](https://github.com/j4321/tkcalendar)
