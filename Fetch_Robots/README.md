# readme

This application is a GUI-based tool to fetch and parse `robots.txt` files from websites. It uses `tkinter` for the graphical interface and supports concurrent fetching of `robots.txt` files for both HTTP and HTTPS protocols. The application is designed to be robust, user-friendly, and helpful for web administrators or developers who need to inspect `robots.txt` files.

---

## Features

- **Domain Normalization**: Validates and normalizes user input for website domains.
- **Robust HTTP Requests**: Implements retry logic with a backoff mechanism to handle network errors gracefully.
- **Parallel Fetching**: Fetches `robots.txt` for both HTTP and HTTPS schemes simultaneously.
- **Error Handling**: Provides detailed error messages for network or input issues.
- **Robots.txt Parsing**: Extracts and displays directives in a structured format.
- **Customizable GUI**:
    - Resizable output display.
    - Adjustable text size for better readability.
    - Interactive buttons and key bindings for ease of use.

---

## Prerequisites

- Python 3.6 or later
- Required Python libraries:
    - `requests`
    - `urllib`
    - `tkinter` (comes pre-installed with Python on most systems)

---

## Installation

1. Clone the repository or copy the script.
2. Install required dependencies by running:
    
    bash
    
    Copy code
    
    `pip install requests`
    
3. Save the script as `robots_fetcher.py` or any preferred name.

---

## Usage

1. Run the script:
    
    bash
    
    Copy code
    
    `python robots_fetcher.py`
    
2. Enter a domain name (e.g., `example.com`) in the input field.
3. Click the "Fetch robots.txt" button or press **Enter** to retrieve the file.
4. View the fetched content and parsed directives in the output area.
5. Adjust the text size using the dropdown for better readability.

---

## GUI Layout

- **Input Section**:
    - Enter a website domain in the text box.
    - A button to fetch the `robots.txt` file.
    - A dropdown to adjust the text size of the output.
- **Output Section**:
    - A scrollable text area to display the fetched `robots.txt` file and parsed directives.

---

## Error Handling

- **Invalid Input**: Displays an error popup if the domain is invalid.
- **Network Errors**: Informs the user of issues like timeouts or server errors.
- **Not Found**: Indicates if the `robots.txt` file is missing.

---

## Contributing

Contributions are welcome! If you find a bug or want to suggest improvements, please create an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. Feel free to use and modify the code.

---

## Example Screenshot

_Add a screenshot of the running GUI application here._

---

Happy Fetching! 🎉
