readme.md

External Link Explorer is a Python-based GUI application that allows users to crawl websites and extract external links. It provides options to display the results on-screen, save them to a file, or both. The application includes a dynamic interface where users can resize the window and adjust font sizes for better readability.

**Features**

- **Crawl Websites:** Extract external links from any website starting from a specified URL.
- **Print and Save Options:** Choose to display links on-screen, save them to a file, or both.
- **Dynamic Font Adjustment:** Increase or decrease font size for better usability.
- **Resizable Output Area:** The output display dynamically adjusts when resizing the window.
- **Customizable Theme:** A sleek dark mode with a black background and white text.

**Prerequisites**

Ensure you have Python 3.x installed along with the following dependencies:

- requests
- bs4 (BeautifulSoup)
- urllib3
- tkinter (built into Python on most platforms)

To install any missing dependencies, use:

![[Pasted image 20250108222213.png]]

How to Run

1. Clone or download this repository.
2. Navigate to the directory containing the script.
3. Run the script:

![[Pasted image 20250108222143.png]]

**Usage**

**Main Features**

1. **Enter URL:** Input the website URL to start crawling. Ensure the URL begins with http:// or https://.
2. **Select Options:**

- Check "Print to screen" to display the external links on-screen (checked by default).
- Check "Save to file" to save the external links to a .txt file.

4. **Start Crawling:** Click the Start Crawl button to begin crawling.
5. **Adjust Font Size:** Use the "Increase Font Size" and "Decrease Font Size" buttons to adjust the font size dynamically.
6. **View Results:**

- Results will appear in the scrollable text area if "Print to screen" is selected.
- If "Save to file" is selected, you'll be prompted to choose a filename and location.

**Example Workflow**

1. Input a URL (e.g., https://example.com).
2. Check "Print to screen" and "Save to file."
3. Click "Start Crawl."
4. Adjust font size as needed.
5. View results in the output area and check the saved file.

**Screenshots**

**Main Interface**

![[Pasted image 20250108222113.png]]

Limitations

- The application does not support JavaScript-rendered content.
- Crawling respects a 1-3 second delay between requests to avoid overwhelming servers.
- Does not follow the robots.txt protocol (can be added in future versions).

**Future Enhancements**

- Add support for rendering JavaScript content (e.g., using Selenium or Playwright).
- Implement robots.txt compliance to respect website crawling rules.
- Provide more customization options for themes and layouts.

**License**

This project is licensed under the MIT License.

**Contributions**

Contributions are welcome! Please feel free to fork this repository and submit a pull request.