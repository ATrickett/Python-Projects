
# URL Scanner Application

## Overview

The **URL Scanner** is a Python-based desktop application that allows users to scan a given URL for external links, JavaScript files, and CSS files. The application provides options to save the extracted information to files and presents the results in an easy-to-use graphical user interface (GUI) built with `Tkinter`.

---

## Features

- **URL Scanning**:
    
    - Extract external links.
    - Identify JavaScript files (both inline and external).
    - Extract CSS files.
- **Customizable Output**:
    
    - Choose which types of files or links to extract.
    - Save results to text files for later use.
- **User-Friendly GUI**:
    
    - Modern and intuitive interface.
    - Adjustable font size for better readability.
- **Error Handling**:
    
    - Graceful handling of network and scanning errors.
    - Informative error messages.

---

## Requirements

- Python 3.7 or newer.
- The following Python packages:
    - `tkinter` (built-in with Python).
    - `requests`.
    - `beautifulsoup4`.

---

## Installation

1. Clone or download the repository:
    
    bash
    
    Copy code
    
    `git clone https://github.com/your-repo/url-scanner.git cd url-scanner`
    
2. Install dependencies:
    
    bash
    
    Copy code
    
    `pip install requests beautifulsoup4`
    
3. Run the application:
    
    bash
    
    Copy code
    
    `python url_scanner.py`
    

---

## Usage

1. **Enter URL**: Type the URL you want to scan in the input box.
2. **Select Options**:
    - `Save to file`: Save the results to text files.
    - `Extract JS files`: Extract JavaScript files.
    - `Extract CSS files`: Extract CSS files.
    - `Extract External Links`: Extract external links.
3. **Start Scan**: Click the "Start Scan" button or press Enter to initiate the scan.
4. **View Results**: The results will appear in the scrollable text area.
5. **Save Results** (Optional): If enabled, the application will save the extracted data to files.

---

## File Structure

bash

Copy code

`. ├── url_scanner.py   # Main application file ├── README.md        # Application documentation`

---

## How It Works

1. **URL Input**: Accepts the URL and validates its format.
2. **HTTP Request**: Fetches the HTML content of the URL.
3. **Parsing**:
    - Extracts external links using `BeautifulSoup`.
    - Extracts JavaScript and CSS files using `BeautifulSoup` and regex.
    - Filters ignored domains based on predefined criteria.
4. **Results**:
    - Displays results in the GUI.
    - Optionally saves results to text files.

---

## Screenshots

_Coming Soon_

---

## Known Limitations

- Requires internet access to scan live URLs.
- Does not process URLs with JavaScript-heavy content (e.g., dynamically rendered pages).

---

## Future Improvements

- Add support for asynchronous requests for faster scans.
- Enhance the GUI with more customization options.
- Include support for scanning local HTML files.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
