

**Assignment Tracker** is a simple and intuitive desktop application to manage assignments and deadlines. Built with Python and Tkinter, it includes features for adding, filtering, editing, and tracking assignments with a user-friendly interface.

## Features

- Add new assignments with details like class, assignment name, due date, and notes.
    
- Filter assignments by:
    
    - Class
        
    - Start and end date
        
- Edit, delete, or mark assignments as completed.
    
- Dynamic, resizable interface with a responsive Treeview.
    
- Default date filtering:
    
    - End date defaults to 30 days from today.
        
- Persistent data storage using SQLite.
    

## Requirements

- Python 3.7 or higher
    
- Required libraries:
    
    - `tkinter` (included in standard Python distribution)
        
    - `tkcalendar`
        
    - `sqlite3` (included in standard Python distribution)
        

### Install Required Libraries

Install any missing libraries using pip:

```
pip install tkcalendar
```

## Installation

### Option 1: Run the Python Script

1. Clone this repository or download the `assignment_tracker.py` file.
    
2. Install Python and the required libraries (see **Requirements**).
    
3. Run the script:
    
    ```
    python assignment_tracker.py
    ```
    

### Option 2: Use the Executable File

1. Download the pre-built executable from the `dist` directory or create it using `PyInstaller` (see **Build Instructions** below).
    
2. Run the `.exe` file directly (no Python installation required).
    

## Build Instructions (Optional)

To create an executable file using PyInstaller:

1. Install PyInstaller:
    
    ```
    pip install pyinstaller
    ```
    
2. Build the executable:
    
    ```
    pyinstaller --onefile --noconsole --name "AssignmentTracker" --key "your_secret_key" assignment_tracker.py
    ```
    
3. The executable will be located in the `dist` directory.
    

## Usage

1. **Adding Assignments**:
    
    - Fill in the details under "Class," "Assignment," "Due Date," and "Notes."
        
    - Click **Add Assignment** to save.
        
2. **Filtering Assignments**:
    
    - Use the "Filter by Class" dropdown to filter by specific classes.
        
    - Set a start and end date for date-based filtering.
        
    - Click **Apply Date Filter**.
        
3. **Managing Assignments**:
    
    - Select an assignment from the table to:
        
        - **Edit**: Update assignment details.
            
        - **Toggle Completion**: Mark as completed or uncompleted.
            
        - **Delete**: Remove the assignment.
            

## Screenshots

_Add screenshots of your application here for better visualization._

## File Structure

- `assignment_tracker.py`: Main application script.
    
- `assignments.db`: SQLite database (created automatically if not present).
    
- `dist/`: Directory containing the executable file (after building with PyInstaller).
    

## Contribution

Contributions are welcome! If you'd like to enhance or fix the app, follow these steps:

1. Fork this repository.
    
2. Create a feature branch:
    
    ```
    git checkout -b feature-name
    ```
    
3. Commit your changes:
    
    ```
    git commit -m "Description of changes"
    ```
    
4. Push to the branch:
    
    ```
    git push origin feature-name
    ```
    
5. Open a pull request.
    

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or feedback, please contact
