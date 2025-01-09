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

visited_lock = Lock()
external_lock = Lock()

# Font settings
DEFAULT_FONT_SIZE = 12

def extract_domain(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return parsed_url.netloc, base_url

def get_external_links(url, visited_pages):
    try:
        response = requests.get(url, headers=HEADERS, verify=False, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        base_domain, _ = extract_domain(url)
        external_links = []
        internal_links = []

        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            full_link = urljoin(url, link)
            link_domain = urlparse(full_link).netloc

            if link_domain and link_domain != base_domain:
                external_links.append(full_link)
            elif link_domain == base_domain and full_link not in visited_pages:
                internal_links.append(full_link)

        return list(set(external_links)), list(set(internal_links))

    except requests.exceptions.RequestException:
        return [], []

def crawl_page(url, visited_pages, all_external_links, pages_to_visit):
    with visited_lock:
        if url in visited_pages:
            return
        visited_pages.add(url)

    external_links, internal_links = get_external_links(url, visited_pages)

    with external_lock:
        all_external_links.update(external_links)

    with visited_lock:
        for link in internal_links:
            if link not in visited_pages and link not in pages_to_visit:
                pages_to_visit.append(link)

    time.sleep(random.uniform(1, 3))

def crawl_website(start_url):
    visited_pages = set()
    all_external_links = set()
    pages_to_visit = [start_url]

    with ThreadPoolExecutor(max_workers=10) as executor:
        while pages_to_visit:
            current_batch = pages_to_visit[:10]
            del pages_to_visit[:10]

            futures = [
                executor.submit(crawl_page, url, visited_pages, all_external_links, pages_to_visit)
                for url in current_batch
            ]

            for future in futures:
                future.result()

    return all_external_links

def save_links_to_file(links, filename="external_links.txt"):
    try:
        with open(filename, "w") as file:
            for link in sorted(links):
                file.write(f"{link}\n")
    except IOError as e:
        print(f"Error saving links to file: {e}")

def start_crawl():
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

        external_links = crawl_website(url)

        if print_var.get():
            result_text.insert(tk.END, "\nExternal links found:\n")
            result_text.insert(tk.END, "\n".join(sorted(external_links)) + "\n")

        if save_var.get():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                save_links_to_file(external_links, filename)
                messagebox.showinfo("Success", f"Links saved to {filename}")
        
        result_text.insert(tk.END, "\nCrawling finished.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Font size adjustment functions
def increase_font_size():
    current_size = text_font['size']
    text_font.configure(size=current_size + 1)

def decrease_font_size():
    current_size = text_font['size']
    text_font.configure(size=max(current_size - 1, 8))  # Prevent font size from getting too small

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
options_frame.grid(row=1, column=0, pady=5, sticky="ew")
options_frame.grid_propagate(False)

print_var = tk.BooleanVar(value=True)
save_var = tk.BooleanVar()

print_check = tk.Checkbutton(options_frame, text="Print to screen", variable=print_var, bg="black", fg="white", selectcolor="gray", font=text_font)
save_check = tk.Checkbutton(options_frame, text="Save to file", variable=save_var, bg="black", fg="white", selectcolor="gray", font=text_font)

print_check.pack(side="left", padx=20)
save_check.pack(side="left", padx=20)

# Crawl Button Section
button_frame = tk.Frame(root, bg="black", height=40)
button_frame.grid(row=2, column=0, pady=5, sticky="ew")
button_frame.grid_propagate(False)

crawl_button = tk.Button(button_frame, text="Start Crawl", command=start_crawl, bg="black", fg="white", font=text_font)
crawl_button.pack(pady=5)

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