import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib3
import time
import random
from threading import Lock

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

IGNORES = [
    "googletags.com", ".wp.org", ".wp.com", ".w3.org",  ".google.com", "googlesyndication.com",
    ".googleapis.com", ".gstatic.com", ".gravatar.com", ".facebook.com",
    ".twitter.com", ".youtube.com", ".vimeo.com", ".linkedin.com", ".instagram.com",
    ".pinterest.com", ".cloudflare.com", ".cloudfront.net", ".jquery.com",
    ".maxcdn.com", ".maxcdncdn.com", ".bootstrapcdn.com", ".fontawesome.com",
    ".fontawesome.io", ".fontawesome.net", ".fontawesome.org", ".fontawesomecdn.com",
    ".fontawesomecdn.net", ".fontawesomecdn.org"
]

visited_lock = Lock()
external_lock = Lock()

# Font settings
DEFAULT_FONT_SIZE = 12

stop_crawl_flag = False

def extract_domain(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return parsed_url.netloc, base_url

def should_ignore(link_domain):
    for ignore in IGNORES:
        if ignore in link_domain:
            return True
    return False

def get_external_links_and_assets(url, visited_pages):
    try:
        response = requests.get(url, headers=HEADERS, verify=False, timeout=5)
        response.raise_for_status()

        # Check content type or XML declaration
        if response.headers.get('Content-Type', '').startswith('application/xml') or response.text.strip().startswith('<?xml'):
            soup = BeautifulSoup(response.content.decode(response.encoding or 'utf-8', errors='replace'), 'xml')
        else:
            soup = BeautifulSoup(response.content.decode(response.encoding or 'utf-8', errors='replace'), 'html.parser')

        base_domain, _ = extract_domain(url)
        external_links = []
        internal_links = []
        js_files = []
        css_files = []

        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            full_link = urljoin(url, link)
            link_domain = urlparse(full_link).netloc

            if link_domain and link_domain != base_domain and not should_ignore(link_domain):
                external_links.append(full_link)
            elif link_domain == base_domain and full_link not in visited_pages:
                internal_links.append(full_link)

        # Extract JS files
        for script_tag in soup.find_all('script', src=True):
            js_files.append(urljoin(url, script_tag['src']))

        # Extract CSS files
        for link_tag in soup.find_all('link', rel="stylesheet", href=True):
            css_files.append(urljoin(url, link_tag['href']))

        return (
            list(set(external_links)),
            list(set(internal_links)),
            list(set(js_files)),
            list(set(css_files))
        )

    except requests.exceptions.RequestException:
        return [], [], [], []

def crawl_page(url, visited_pages, all_external_links, pages_to_visit, all_js_files, all_css_files):
    global stop_crawl_flag

    if stop_crawl_flag:
        return

    with visited_lock:
        if url in visited_pages:
            return
        visited_pages.add(url)

    external_links, internal_links, js_files, css_files = get_external_links_and_assets(url, visited_pages)

    with external_lock:
        all_external_links.update(external_links)
        all_js_files.update(js_files)
        all_css_files.update(css_files)

    with visited_lock:
        for link in internal_links:
            if link not in visited_pages and link not in pages_to_visit:
                pages_to_visit.append(link)

    time.sleep(random.uniform(1, 3))

def crawl_website(start_url):
    global stop_crawl_flag

    visited_pages = set()
    all_external_links = set()
    all_js_files = set()
    all_css_files = set()
    pages_to_visit = [start_url]

    with ThreadPoolExecutor(max_workers=10) as executor:
        while pages_to_visit and not stop_crawl_flag:
            current_batch = pages_to_visit[:10]
            del pages_to_visit[:10]

            futures = [
                executor.submit(
                    crawl_page, url, visited_pages, all_external_links, pages_to_visit, all_js_files, all_css_files
                )
                for url in current_batch
            ]

            for future in futures:
                future.result()

    return all_external_links, all_js_files, all_css_files

def save_links_to_file(links, filename):
    try:
        with open(filename, "w") as file:
            for link in sorted(links):
                file.write(f"{link}\n")
    except IOError as e:
        print(f"Error saving links to file: {e}")

def start_crawl():
    global stop_crawl_flag
    stop_crawl_flag = False

    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Crawling started...\n")
        root.update_idletasks()

        external_links, js_files, css_files = crawl_website(url)

        if external_link_var.get():
            result_text.insert(tk.END, "\nExternal links found:\n")
            result_text.insert(tk.END, "\n".join(sorted(external_links)) + "\n")

        if js_var.get():
            result_text.insert(tk.END, "\nJavaScript files found:\n")
            result_text.insert(tk.END, "\n".join(sorted(js_files)) + "\n")

        if css_var.get():
            result_text.insert(tk.END, "\nCSS files found:\n")
            result_text.insert(tk.END, "\n".join(sorted(css_files)) + "\n")

        if save_var.get():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                save_links_to_file(external_links, filename + "_external_links.txt")
                save_links_to_file(js_files, filename + "_js_files.txt")
                save_links_to_file(css_files, filename + "_css_files.txt")
                messagebox.showinfo("Success", f"Links saved to {filename}_*.txt")

        result_text.insert(tk.END, "\nCrawling finished.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def stop_crawl():
    global stop_crawl_flag
    stop_crawl_flag = True
    result_text.insert(tk.END, "\nCrawling stopped by user.\n")

# Font size adjustment functions
def increase_font_size():
    current_size = text_font['size']
    text_font.configure(size=current_size + 1)

def decrease_font_size():
    current_size = text_font['size']
    text_font.configure(size=max(current_size - 1, 8))

# Initialize GUI
root = tk.Tk()
root.title("External Link Explorer")
root.configure(bg="black")

# Configure grid layout for resizing
root.columnconfigure(0, weight=1)
root.rowconfigure(3, weight=1)

# Initialize font
text_font = font.Font(family="Helvetica", size=DEFAULT_FONT_SIZE)

# URL Input Section
frame = tk.Frame(root, bg="black", height=60)
frame.grid(row=0, column=0, pady=5, sticky="ew")
frame.grid_propagate(False)

url_label = tk.Label(frame, text="Enter URL:", bg="black", fg="white", font=text_font)
url_label.grid(row=0, column=0, padx=5, pady=10)

url_entry = tk.Entry(frame, width=50, bg="black", fg="white", insertbackground="white", font=text_font)
url_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

frame.columnconfigure(1, weight=1)

# Options Section (Check Buttons)
options_frame = tk.Frame(root, bg="black", height=50)
options_frame.grid(row=1, column=0, pady=5, sticky="nsew")

# Configure grid layout for options_frame
options_frame.columnconfigure(0, weight=1)
options_frame.columnconfigure(1, weight=1)
options_frame.columnconfigure(2, weight=1)
options_frame.columnconfigure(3, weight=1)

save_var = tk.BooleanVar()
js_var = tk.BooleanVar()
css_var = tk.BooleanVar()
external_link_var = tk.BooleanVar()

save_check = tk.Checkbutton(options_frame, text="Save to file", variable=save_var, bg="black", fg="white", selectcolor="gray", font=text_font)
js_check = tk.Checkbutton(options_frame, text="Extract JS files", variable=js_var, bg="black", fg="white", selectcolor="gray", font=text_font)
css_check = tk.Checkbutton(options_frame, text="Extract CSS files", variable=css_var, bg="black", fg="white", selectcolor="gray", font=text_font)
external_link_check = tk.Checkbutton(options_frame, text="Extract External Links", variable=external_link_var, bg="black", fg="white", selectcolor="gray", font=text_font)

save_check.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
js_check.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
css_check.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
external_link_check.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

# Crawl Button Section
button_frame = tk.Frame(root, bg="black", height=40)
button_frame.grid(row=2, column=0, pady=5, sticky="n")
button_frame.grid_propagate(False)

crawl_button = tk.Button(button_frame, text="Start Crawl", command=start_crawl, bg="black", fg="white", font=text_font)
crawl_button.pack(side="left", padx=10, pady=5)

stop_button = tk.Button(button_frame, text="Stop Crawl", command=stop_crawl, bg="black", fg="white", font=text_font)
stop_button.pack(side="left", padx=10, pady=5)

# Font Size Adjustment Buttons
font_frame = tk.Frame(root, bg="black", height=40)
font_frame.grid(row=4, column=0, pady=5, sticky="ew")
font_frame.grid_propagate(False)

increase_font_button = tk.Button(font_frame, text="Increase Font Size", command=increase_font_size, bg="black", fg="white", font=text_font)
increase_font_button.pack(side="left", padx=10)

decrease_font_button = tk.Button(font_frame, text="Decrease Font Size", command=decrease_font_size, bg="black", fg="white", font=text_font)
decrease_font_button.pack(side="left", padx=10)

# Results Section (Resizable)
result_text = scrolledtext.ScrolledText(root, width=80, height=20, bg="black", fg="white", insertbackground="white", font=text_font)
result_text.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

root.rowconfigure(3, weight=1)

root.mainloop()
