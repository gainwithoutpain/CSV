import tkinter as tk
from tkinter import filedialog, messagebox
import csv

class TextUpdater:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Updater")

        # Selecting Input File
        self.input_file_path = None
        self.select_input_button = tk.Button(root, text="Select Input Text File", command=self.select_input_file)
        self.select_input_button.pack(pady=10)

        # Input for Match Value
        self.match_label = tk.Label(root, text="Value to Match (1st column):")
        self.match_label.pack(pady=5)
        self.match_entry = tk.Entry(root)
        self.match_entry.pack(pady=5)

        # Input for New Value
        self.new_label = tk.Label(root, text="New Value (5th column):")
        self.new_label.pack(pady=5)
        self.new_entry = tk.Entry(root)
        self.new_entry.pack(pady=5)

        # Update Button
        self.update_button = tk.Button(root, text="Update File", command=self.update_file)
        self.update_button.pack(pady=20)

        # Changes Display
        self.changes_text = tk.Text(root, height=10, width=50)
        self.changes_text.pack(pady=10)

    def select_input_file(self):
        self.input_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.input_file_path:
            messagebox.showinfo("File Selected", f"{self.input_file_path} selected.")

    def update_file(self):
        if not self.input_file_path:
            messagebox.showwarning("Warning", "Please select an input text file.")
            return

        match_value = self.match_entry.get().strip()
        new_value = self.new_entry.get().strip()

        if not match_value or not new_value:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        changes = []
        with open(self.input_file_path, newline='') as infile:
            reader = csv.reader(infile, delimiter='\t')  # Changed for tab-delimited text file
            updated_rows = []
            
            for row in reader:
                if row and row[0] == match_value:
                    # Store the change
                    old_value = row[4] if len(row) >= 5 else "N/A"
                    changes.append(f"Changed from '{old_value}' to '{new_value}'")
                    
                    # Replace the value in the 5th column (index 4)
                    if len(row) >= 5:
                        row[4] = new_value
                updated_rows.append(row)

        # Overwrite the original file with the updated data
        with open(self.input_file_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter='\t')  # Again, use tab as delimiter
            writer.writerows(updated_rows)

        # Display changes
        self.changes_text.delete(1.0, tk.END)  # Clear previous text
        if changes:
            self.changes_text.insert(tk.END, "Changes made:\n" + "\n".join(changes))
        else:
            self.changes_text.insert(tk.END, "No matches found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextUpdater(root)
    root.mainloop()