# URL Scanner

## Overview

The **URL Scanner** is a Python-based GUI application that analyzes a single web page for external links, JavaScript files, and CSS files. It uses the `requests` library to fetch the web page content and `BeautifulSoup` for parsing HTML. The application is user-friendly and supports saving extracted links to files.

## Features

- **URL Analysis**: Scans the provided URL for external links, JavaScript files, and CSS files.
    
- **Save Results**: Option to save extracted data into text files.
    
- **Customizable Options**: Choose to extract specific types of data (e.g., external links, JS, CSS).
    
- **Font Adjustment**: Adjust the font size of the result display.
    
- **Keyboard Shortcut**: Press `Enter` after typing the URL to start the scan.
    

## Requirements

- Python 3.6+
    
- Libraries:
    
    - `tkinter`
        
    - `requests`
        
    - `beautifulsoup4`
        
    - `urllib3`
        

## Installation

1. Clone or download this repository.
    
2. Install required libraries using pip:
    
    ```
    pip install requests beautifulsoup4
    ```
    
3. Run the application:
    
    ```
    python url_scanner.py
    ```
    

## Usage

1. Launch the application.
    
2. Enter a URL in the input field.
    
3. Check the options for data extraction (e.g., external links, JS, CSS).
    
4. Click the **Start Scan** button or press `Enter` to begin scanning.
    
5. View results in the scrolling text area.
    
6. (Optional) Save results to a file by selecting the "Save to file" option.
    

## GUI Layout

- **URL Input Section**: Input field for entering the URL.
    
- **Options Section**: Checkboxes to select data to extract.
    
- **Scan Button Section**: Buttons to start the scan.
    
- **Font Adjustment Section**: Buttons to adjust font size.
    
- **Results Section**: Displays the extracted data in a scrollable area.
    

## Example

1. Enter the URL: `https://example.com`
    
2. Check options to extract external links and CSS files.
    
3. Press `Enter` or click **Start Scan**.
    
4. Results display in the text area.
    

## Error Handling

- The application alerts the user with a message box if an error occurs, such as an invalid URL or network issues.
    

## Customization

Modify the `IGNORES` list in the code to exclude specific domains from being extracted as external links.

## License

This project is licensed under the MIT License.

## Contribution

Feel free to fork the repository and submit pull requests for enhancements or bug fixes.

---

For any issues or feature requests, please create an issue in the GitHub repository.
