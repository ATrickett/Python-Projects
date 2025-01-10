# External Link Explorer

## Overview

The Website Crawler Application is a Python-based tool with a graphical user interface (GUI) built using `tkinter`. It enables users to crawl websites starting from a given URL, extracting:

- External links
- JavaScript files
- CSS files

The application includes a multithreaded crawling mechanism for efficiency, dynamic layout for user interface responsiveness, and advanced options to customize the crawl.

---

## Features

### **Graphical User Interface (GUI)**

- User-friendly design with dynamic resizing capabilities.
- Built using `tkinter`.

### **Crawling Functionality**

- Extracts:
    - **External links**: Links to pages outside the base domain.
    - **JavaScript files**: Links to `.js` files.
    - **CSS files**: Links to `.css` files.
- Follows internal links to ensure comprehensive crawling.
- Filters out predefined domains (e.g., social media, trackers).

### **Multithreaded Crawling**

- Uses `ThreadPoolExecutor` to crawl multiple pages concurrently, improving performance.

### **Customizable Options**

- **Save to file**: Save results to `.txt` files.
- **Extract JS files**: Enable or disable JavaScript file extraction.
- **Extract CSS files**: Enable or disable CSS file extraction.
- **Extract External Links**: Toggle external link extraction and display.

### **Dynamic Layout**

- Components resize and adjust dynamically with the window.
- Checkbuttons and text areas maintain usability across screen sizes.

### **Crawl Stopping Capability**

- **Stop Crawl** button instantly halts the crawling process.

### **Result Display**

- Results are displayed in a scrollable text box for easy viewing.
- Includes external links, JavaScript files, and CSS files based on user preferences.

### **Error Handling**

- Provides clear error messages for invalid URLs or network issues.

### **File Saving**

- Allows saving extracted links to `.txt` files with user-specified filenames.

### **Font Size Adjustment**

- Includes buttons to increase or decrease the font size for better accessibility.

### **Request Handling**

- Suppresses HTTPS certificate warnings.
- Adds random delays between requests to avoid overwhelming servers.

---

## Installation

1. Clone this repository:
    
    ```bash
    git clone https://github.com/your-repo/website-crawler.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd website-crawler
    ```
    
3. Install dependencies using `pip`:
    
    ```bash
    pip install -r requirements.txt
    ```
    
    **Note**: Ensure you have Python 3.7 or later installed.

---

## Usage

1. Run the application:
    
    ```bash
    python website_crawler.py
    ```
    
2. Enter the URL to start crawling.
3. Customize options:
    - Enable or disable JavaScript, CSS, or external link extraction.
    - Choose whether to save results to files.
4. Click **Start Crawl** to begin crawling.
5. View results in the scrollable text area or save them to files.
6. Use **Stop Crawl** to halt the process if necessary.

---

## Example Output

Results are displayed in the application and saved as `.txt` files if the "Save to file" option is enabled.

### Example:

#### In-App Display:

```
Crawling started...

External links found:
https://example.com/page1
https://example.com/page2

JavaScript files found:
https://example.com/static/js/script.js

CSS files found:
https://example.com/static/css/style.css

Crawling finished.
```

#### Saved Files:

- `external_links.txt`
- `js_files.txt`
- `css_files.txt`

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Open a pull request describing your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://chatgpt.com/g/g-cKXjWStaE-python/c/LICENSE) file for details.

---

## Acknowledgments

- Built with `tkinter` for GUI.
- Utilizes `requests` and `BeautifulSoup` for web scraping.

---

## Contact

For questions or feedback, please contact:

- Name: Aaron Trickett
    
- GitHub: [https://github.com/ATrickett]
