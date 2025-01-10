import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib3
import re

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
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

DEFAULT_FONT_SIZE = 12

def should_ignore(link_domain):
    for ignore in IGNORES:
        if ignore in link_domain:
            return True
    return False

def scan_url(url):
    try:
        response = requests.get(url, headers=HEADERS, verify=False, timeout=5)
        response.raise_for_status()

        # Decode HTML content
        html_content = response.content.decode(response.encoding or 'utf-8', errors='replace')
        soup = BeautifulSoup(html_content, 'html.parser')

        base_domain = urlparse(url).netloc
        external_links = set()
        js_files = set()
        css_files = set()

        # Extract structured data using BS4
        for a_tag in soup.find_all('a', href=True):
            full_link = urljoin(url, a_tag['href'])
            if base_domain not in full_link and not should_ignore(urlparse(full_link).netloc):
                external_links.add(full_link)

        for script_tag in soup.find_all('script'):
            if script_tag.has_attr('src'):  # External JS
                js_files.add(urljoin(url, script_tag['src']))
            elif script_tag.string:  # Inline JS
                js_files.add(f"INLINE: {script_tag.string.strip()}")

        for link_tag in soup.find_all('link', rel='stylesheet', href=True):
            css_files.add(urljoin(url, link_tag['href']))

        # Use regex for unstructured data (e.g., additional JS URLs)
        js_url_matches = re.findall(r"https?://[^\s\"'>]+\.js", html_content)
        js_files.update(js_url_matches)

        return sorted(external_links), sorted(js_files), sorted(css_files)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to scan URL: {e}")
        return [], [], []

def start_scan(event=None):
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Scanning URL...\n")
        root.update_idletasks()

        external_links, js_files, css_files = scan_url(url)

        if external_link_var.get():
            result_text.insert(tk.END, "\nExternal links found:\n")
            result_text.insert(tk.END, "\n".join(sorted(external_links)) + "\n")

        if js_var.get():
            result_text.insert(tk.END, "\nJavaScript files found (including inline):\n")
            for js in sorted(js_files):
                if js.startswith("INLINE: "):
                    result_text.insert(tk.END, f"\n--- Inline JS ---\n{js[8:]}\n")
                else:
                    result_text.insert(tk.END, js + "\n")

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
                messagebox.showinfo("Success", f"Links and scripts saved to {filename}_*.txt")

        result_text.insert(tk.END, "\nScanning finished.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def save_links_to_file(links, filename):
    try:
        with open(filename, "w") as file:
            for link in sorted(links):
                file.write(f"{link}\n")
    except IOError as e:
        print(f"Error saving links to file: {e}")

# Initialize GUI
root = tk.Tk()
root.title("URL Scanner")
root.configure(bg="black")

# Configure grid resizing
root.columnconfigure(0, weight=1)
root.rowconfigure(3, weight=1)

# Initialize font
text_font = font.Font(family="Helvetica", size=DEFAULT_FONT_SIZE)

# Font size adjustment functions
def increase_font_size():
    current_size = text_font['size']
    text_font.configure(size=current_size + 1)

def decrease_font_size():
    current_size = text_font['size']
    text_font.configure(size=max(current_size - 1, 8))

# Context menu for right-click paste in URL entry
def paste_text(event=None):
    try:
        url_entry.delete(0, tk.END)  # Clear existing content
        url_entry.insert(0, root.clipboard_get())  # Paste content from clipboard
    except tk.TclError:
        pass  # Ignore errors (e.g., if clipboard is empty)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Paste", command=paste_text)

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

# URL Input Section
frame = tk.Frame(root, bg="black", height=60)
frame.grid(row=0, column=0, pady=5, sticky="ew")
frame.columnconfigure(1, weight=1)

url_label = tk.Label(frame, text="Enter URL:", bg="black", fg="white", font=text_font)
url_label.grid(row=0, column=0, padx=5, pady=10)

url_entry = tk.Entry(frame, width=50, bg="black", fg="white", insertbackground="white", font=text_font)
url_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
url_entry.bind("<Return>", start_scan)
url_entry.bind("<Button-3>", show_context_menu)

# Options Section
options_frame = tk.Frame(root, bg="black")
options_frame.grid(row=1, column=0, pady=5, sticky="nsew")
options_frame.columnconfigure((0, 1, 2, 3), weight=1)

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

# Scan Button Section
button_frame = tk.Frame(root, bg="black")
button_frame.grid(row=2, column=0, pady=5, sticky="ew")

scan_button = tk.Button(button_frame, text="Start Scan", command=start_scan, bg="black", fg="white", font=text_font)
scan_button.pack(side="left", padx=10, pady=5)

# Font Size Adjustment Buttons
font_frame = tk.Frame(root, bg="black")
font_frame.grid(row=4, column=0, pady=5, sticky="ew")

increase_font_button = tk.Button(font_frame, text="Increase Font Size", command=increase_font_size, bg="black", fg="white", font=text_font)
increase_font_button.pack(side="left", padx=10)

decrease_font_button = tk.Button(font_frame, text="Decrease Font Size", command=decrease_font_size, bg="black", fg="white", font=text_font)
decrease_font_button.pack(side="left", padx=10)

# Results Section
result_text = scrolledtext.ScrolledText(root, bg="black", fg="white", insertbackground="white", font=text_font)
result_text.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

root.mainloop()
