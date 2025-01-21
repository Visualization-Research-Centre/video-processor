import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter")

        # File selection
        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Output format options
        self.format_var = tk.StringVar(value="mp4")
        self.format_label = tk.Label(root, text="Select output format:")
        self.format_label.pack(pady=5)

        self.format_options = ["mp4", "avi", "mkv", "mov"]
        for format_option in self.format_options:
            tk.Radiobutton(root, text=format_option, variable=self.format_var, value=format_option).pack(anchor=tk.W)

        # Convert button
        self.convert_button = tk.Button(root, text="Convert", command=self.convert_file)
        self.convert_button.pack(pady=20)

        self.input_file = None

    def browse_file(self):
        self.input_file = filedialog.askopenfilename()
        if self.input_file:
            self.file_label.config(text=os.path.basename(self.input_file))

    def convert_file(self):
        if not self.input_file:
            messagebox.showerror("Error", "No file selected")
            return

        output_format = self.format_var.get()
        output_file = filedialog.asksaveasfilename(defaultextension=f".{output_format}", filetypes=[(f"{output_format.upper()} files", f"*.{output_format}")])

        if not output_file:
            return

        # Run ffmpeg in background
        command = ["ffmpeg", "-i", self.input_file, output_file]
        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", f"File converted successfully to {output_format.upper()}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to convert file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()
