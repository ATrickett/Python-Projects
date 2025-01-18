import tkinter as tk
from tkinter import filedialog, messagebox
import csv

def validate_input(char):
    """Validates that the input is either 'a', 'b', 'c', 'd', 'e', '0', '1', '2', '3', '4', '5', or empty."""
    return char in ('a', 'b', 'c', 'd', 'e', '0', '1', '2', '3', '4', '5', '')

def export_to_csv():
    """Exports the input data to a CSV file."""
    # Collect data from all input boxes
    data = [entry.get() for entry in entries]

    # Ask the user for a file location to save the CSV
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save as"
    )
    
    if file_path:
        try:
            # Write data to the CSV file
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Box Number", "Value"])  # Header row
                for i, value in enumerate(data, start=1):
                    writer.writerow([i, value])
            messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export data: {e}")

# Create the main application window
root = tk.Tk()
root.title("Answer Sheet")

# List to hold entry widgets
entries = []

# Create a frame for input boxes
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Add 100 labeled input boxes in 4 columns of 25 each
for i in range(100):
    row = i % 25
    col = i // 25
    
    label = tk.Label(frame, text=f"{i + 1}:")
    label.grid(row=row, column=col * 2, padx=5, pady=2, sticky="e")
    
    entry = tk.Entry(frame, validate="key")
    entry.grid(row=row, column=col * 2 + 1, padx=5, pady=2)
    entry['validatecommand'] = (root.register(validate_input), '%S')
    
    entries.append(entry)

# Export button
export_button = tk.Button(root, text="Export to CSV", command=export_to_csv)
export_button.pack(pady=10)

# Start the application
root.mainloop()
