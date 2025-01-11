import requests
from urllib.parse import urlparse
import concurrent.futures
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def normalize_url(url):
    url = url.strip().rstrip('/')
    parsed_url = urlparse(url)
    if not parsed_url.netloc and not parsed_url.path:
        raise ValueError("Invalid input URL. Please enter a valid domain (e.g., example.com).")
    return parsed_url.netloc or parsed_url.path

def create_session_with_retries():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_robots(url):
    try:
        session = create_session_with_retries()
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            return "robots.txt not found."
        return f"Failed to fetch robots.txt. HTTP status: {response.status_code}"
    except requests.RequestException as e:
        return handle_request_error(e)

def fetch_robots_in_parallel(domain):
    schemes = ["https", "http"]
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_scheme = {executor.submit(fetch_robots, f"{scheme}://{domain}/robots.txt"): scheme for scheme in schemes}
        for future in concurrent.futures.as_completed(future_to_scheme):
            scheme = future_to_scheme[future]
            try:
                results[scheme] = future.result()
            except Exception as exc:
                results[scheme] = f"Failed with error: {exc}"
    return results

def handle_request_error(exception):
    if isinstance(exception, requests.Timeout):
        return "Request timed out. Please check your network and try again."
    elif isinstance(exception, requests.ConnectionError):
        return "Failed to connect to the server. Please check the URL."
    return f"An unexpected error occurred: {exception}"

def parse_robots_txt(content):
    directives = {}
    for line in content.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip()
            directives.setdefault(key, []).append(value)
    return directives

def fetch_and_display():
    domain = entry.get()
    try:
        domain = normalize_url(domain)
        results = fetch_robots_in_parallel(domain)
        output.delete(1.0, tk.END)
        for scheme, result in results.items():
            output.insert(tk.END, f"\n--- Results for {scheme.upper()} ---\n")
            if "not found" in result.lower() or "error" in result.lower():
                output.insert(tk.END, result + "\n")
            else:
                output.insert(tk.END, "robots.txt content:\n" + result + "\n")
                directives = parse_robots_txt(result)
                output.insert(tk.END, "\nParsed Directives:\n")
                for key, values in directives.items():
                    output.insert(tk.END, f"{key}: {', '.join(values)}\n")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

def update_text_size(event):
    selected_size = text_size_var.get()
    output.config(font=("TkDefaultFont", selected_size))

# GUI Setup
root = tk.Tk()
root.title("robots.txt Fetcher")

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

label = tk.Label(frame, text="Enter Website Domain:", font=("TkDefaultFont", 12))
label.pack(side=tk.LEFT, padx=5)

entry = tk.Entry(frame, width=40)
entry.bind('<Return>', lambda event: fetch_and_display())
entry.pack(side=tk.LEFT, padx=5)

fetch_button = tk.Button(frame, text="Fetch robots.txt", command=fetch_and_display, font=("TkDefaultFont", 12))
fetch_button.pack(side=tk.LEFT, padx=5)

# Text Size Dropdown
text_size_var = tk.IntVar(value=12)
size_label = tk.Label(frame, text="Text Size:", font=("TkDefaultFont", 12))
size_label.pack(side=tk.LEFT, padx=5)

text_size_dropdown = ttk.Combobox(frame, textvariable=text_size_var, values=[8, 10, 12, 14, 16, 18, 20])
text_size_dropdown.pack(side=tk.LEFT, padx=5)
text_size_dropdown.bind("<<ComboboxSelected>>", update_text_size)

# Output Frame
output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=30, height=20, font=("TkDefaultFont", 12))
output.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Allow resizing of the output display
root.rowconfigure(1, weight=1)

# Run the GUI loop
root.mainloop()
