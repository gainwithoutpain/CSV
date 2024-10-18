import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class PyInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python to EXE Converter")

        self.label = tk.Label(root, text="Select a Python file to convert to EXE:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Python File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert to EXE", command=self.convert_to_exe, state=tk.DISABLED)
        self.convert_button.pack(pady=5)

        self.file_path = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if self.file_path:
            self.convert_button.config(state=tk.NORMAL)

    def convert_to_exe(self):
        if self.file_path:
            # Get the directory and filename without extension
            directory, filename = os.path.split(self.file_path)
            base_filename = os.path.splitext(filename)[0]

            # Command to create executable
            command = f"pyinstaller --onefile --distpath {directory} {self.file_path}"

            # Run the command
            try:
                subprocess.run(command, check=True, shell=True)
                messagebox.showinfo("Success", f"Executable created at: {directory}/{base_filename}.exe")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to create executable:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyInstallerGUI(root)
    root.mainloop()