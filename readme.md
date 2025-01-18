**Answer Sheet** is a simple graphical user interface (GUI) application built with Python and `tkinter`. It allows users to input answers into 100 labeled input fields and export the data to a CSV file. The application enforces input validation to accept only specific characters.

## Features

- **100 Input Fields**: Organized in 4 columns with 25 fields per column, each labeled with a number.
    
- **Input Validation**: Accepts only the characters `a`, `b`, `c`, `d`, `e`, `0`, `1`, `2`, `3`, `4`, `5`.
    
- **CSV Export**: Save the entered answers to a CSV file with labeled rows.
    
- **Standalone Application**: Can be converted to an executable using `pyinstaller` (e.g., `Answer_Sheet.exe`).
    

## Installation

### Requirements

- Python 3.x
    
- The following libraries (included with Python by default):
    
    - `tkinter`
        
    - `csv`
        
    - `tkinter.messagebox`
        

### Clone or Download the Repository

```
git clone <repository-url>
cd Answer_Sheet
```

### Run the Application

1. Ensure you have Python 3.x installed.
    
2. Run the application with:
    
    ```
    python Answer_Sheet.py
    ```
    

### Convert to Executable

To create a standalone executable file:

1. Install `pyinstaller` if not already installed:
    
    ```
    pip install pyinstaller
    ```
    
2. Run the following command to generate the `.exe` file:
    
    ```
    pyinstaller --noconsole --onefile --name Answer_Sheet Answer_Sheet.py
    ```
    
3. The `Answer_Sheet.exe` file will be available in the `dist` folder.
    

## Usage

1. Open the application (run the Python script or the standalone executable).
    
2. Enter valid characters (`a`, `b`, `c`, `d`, `e`, `0`, `1`, `2`, `3`, `4`, `5`) into the input fields.
    
3. Click the **Export to CSV** button to save your entries as a CSV file.
    

### CSV Format

The exported CSV file includes:

- **Column 1**: Box Number
    
- **Column 2**: Value entered into the corresponding box
    

Example:

```
Box Number,Value
1,a
2,b
3,1
...
```

## Screenshots

_(Replace with an actual screenshot if available)_

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.