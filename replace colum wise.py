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

        # Input for Match Column
        self.match_col_label = tk.Label(root, text="Match Column Number (1-based):")
        self.match_col_label.pack(pady=5)
        self.match_col_entry = tk.Entry(root)
        self.match_col_entry.pack(pady=5)

        # Input for New Value Column
        self.replace_col_label = tk.Label(root, text="Replace Column Number (1-based):")
        self.replace_col_label.pack(pady=5)
        self.replace_col_entry = tk.Entry(root)
        self.replace_col_entry.pack(pady=5)

        # Checkbox for using a second file for replacements
        self.use_file_checkbox_var = tk.BooleanVar()
        self.use_file_checkbox = tk.Checkbutton(root, text="Use another file for replacements",
                                                  variable=self.use_file_checkbox_var, command=self.toggle_input_fields)
        self.use_file_checkbox.pack(pady=5)

        # Button to select the file for replacements
        self.select_replacement_file_button = tk.Button(root, text="Select Replacement Values File",
                                                        command=self.select_replacement_file, state=tk.DISABLED)
        self.select_replacement_file_button.pack(pady=10)

        # Input for Match Value
        self.match_value_label = tk.Label(root, text="Value to Match (Disabled if using file):")
        self.match_value_label.pack(pady=5)
        self.match_value_entry = tk.Entry(root)
        self.match_value_entry.pack(pady=5)

        # Input for New Value
        self.new_value_label = tk.Label(root, text="New Value (Disabled if using file):")
        self.new_value_label.pack(pady=5)
        self.new_value_entry = tk.Entry(root)
        self.new_value_entry.pack(pady=5)

        # Update Button
        self.update_button = tk.Button(root, text="Update File", command=self.update_file)
        self.update_button.pack(pady=20)

        # Changes Display
        self.changes_text = tk.Text(root, height=10, width=50)
        self.changes_text.pack(pady=10)

        self.replacement_file_path = None

    def toggle_input_fields(self):
        if self.use_file_checkbox_var.get():
            # Disable the entry fields for values to match and new values
            self.select_replacement_file_button.config(state=tk.NORMAL)
            self.match_value_entry.config(state=tk.DISABLED)
            self.new_value_entry.config(state=tk.DISABLED)
            self.match_col_entry.config(state=tk.NORMAL)  # Keep column entry enabled
            self.replace_col_entry.config(state=tk.NORMAL)  # Keep column entry enabled
        else:
            # Enable the entry fields for values to match and new values
            self.select_replacement_file_button.config(state=tk.DISABLED)
            self.match_value_entry.config(state=tk.NORMAL)
            self.new_value_entry.config(state=tk.NORMAL)
            self.match_col_entry.config(state=tk.NORMAL)  # Keep column entry enabled
            self.replace_col_entry.config(state=tk.NORMAL)  # Keep column entry enabled

    def select_input_file(self):
        self.input_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.input_file_path:
            messagebox.showinfo("File Selected", f"{self.input_file_path} selected.")

    def select_replacement_file(self):
        self.replacement_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.replacement_file_path:
            messagebox.showinfo("File Selected", f"{self.replacement_file_path} selected.")

    def update_file(self):
        if not self.input_file_path:
            messagebox.showwarning("Warning", "Please select an input text file.")
            return

        if self.use_file_checkbox_var.get():
            # Use the replacement file
            if not self.replacement_file_path:
                messagebox.showwarning("Warning", "Please select a replacement values file.")
                return

            replacements = {}
            with open(self.replacement_file_path, newline='') as repl_file:
                repl_reader = csv.reader(repl_file, delimiter='\t')
                for row in repl_reader:
                    if row and len(row) >= 2:
                        replacements[row[0]] = row[1]  # First column for matching, second for new value

            changes = []
            with open(self.input_file_path, newline='') as infile:
                reader = csv.reader(infile, delimiter='\t')
                updated_rows = []
                
                for row in reader:
                    if row and len(row) > 0 and row[0] in replacements:
                        old_value = row[1] if len(row) > 1 else "N/A"
                        new_value = replacements[row[0]]
                        changes.append(f"Changed from '{old_value}' to '{new_value}'")
                        if len(row) > 1:
                            row[1] = new_value  # Replace with the new value from the replacement file
                    updated_rows.append(row)

            with open(self.input_file_path, 'w', newline='') as outfile:
                writer = csv.writer(outfile, delimiter='\t')
                writer.writerows(updated_rows)

            self.display_changes(changes)

        else:
            # Use the columns from user input
            try:
                match_col = int(self.match_col_entry.get().strip()) - 1  # Convert to 0-based index
                replace_col = int(self.replace_col_entry.get().strip()) - 1  # Convert to 0-based index
            except ValueError:
                messagebox.showwarning("Warning", "Please enter valid column numbers.")
                return

            match_value = self.match_value_entry.get().strip()
            new_value = self.new_value_entry.get().strip()

            if not match_value or new_value == "":
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return

            changes = []
            with open(self.input_file_path, newline='') as infile:
                reader = csv.reader(infile, delimiter='\t')
                updated_rows = []
                
                for row in reader:
                    if row and len(row) > match_col and row[match_col] == match_value:
                        old_value = row[replace_col] if len(row) > replace_col else "N/A"
                        changes.append(f"Changed from '{old_value}' to '{new_value}'")
                        if len(row) > replace_col:
                            row[replace_col] = new_value
                    updated_rows.append(row)

            with open(self.input_file_path, 'w', newline='') as outfile:
                writer = csv.writer(outfile, delimiter='\t')
                writer.writerows(updated_rows)

            self.display_changes(changes)

    def display_changes(self, changes):
        self.changes_text.delete(1.0, tk.END)  # Clear previous text
        if changes:
            self.changes_text.insert(tk.END, "Changes made:\n" + "\n".join(changes))
        else:
            self.changes_text.insert(tk.END, "No matches found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TextUpdater(root)
    root.mainloop()