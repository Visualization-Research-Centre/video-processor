import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import datetime

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter")

        # File selection
        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.pack(pady=10)
        
        # CRF number input
        self.vbr_label = tk.Label(root, text="Enter bit rate number in Mbit/s (leave empty for no specification):")
        self.vbr_label.pack(pady=5)
        self.vbr_entry = tk.Entry(root)
        self.vbr_entry.pack(pady=5)
        
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

        self.input_files = None

    def browse_file(self):
        self.input_files = filedialog.askopenfilenames()
        if len(self.input_files) == 1:
            self.file_label.config(text=os.path.basename(self.input_files[0]))
        else:
            self.file_label.config(text=f"{len(self.input_files)} files selected")

    def convert_file(self):
        if not self.input_files:
            messagebox.showerror("Error", "No file selected")
            return
        
        output_format = self.format_var.get()
        video_bitrate = self.vbr_entry.get()
        
        if video_bitrate == "":
            video_bitrate = ""
        else:
            video_bitrate = f"-b:v {video_bitrate}M"
            
        
        for i, input_file in enumerate(self.input_files):
            
            # get output file name
            output_file = os.path.splitext(input_file)[0] + f"hap_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{output_format}"
            
            print(f"Converting {input_file} to {output_file}")

            command = ["ffmpeg", "-i", input_file, "-c:v", "hap", output_file]
            
            try:
                subprocess.run(command, check=True)
                messagebox.showinfo("Success", f"File converted successfully to {output_format.upper()}: {output_file}")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to convert file: {e}")
        
        
        # get output file name
        # output_file = filedialog.asksaveasfilename(defaultextension=f".{output_format}", filetypes=[(f"{output_format.upper()} files", f"*.{output_format}")])
        # if not output_file:
        #     return

        # Run ffmpeg in background
        # crf_value = self.vbr_entry.get()
        # if not crf_value.isdigit() or not (0 <= int(crf_value) <= 51):
        #     messagebox.showerror("Error", "Invalid CRF value. Please enter a number between 0 and 51.")
        #     return

        # command = ["ffmpeg", "-i", self.input_files, "-c:v hap", output_file]
        # try:
        #     subprocess.run(command, check=True)
        #     messagebox.showinfo("Success", f"File converted successfully to {output_format.upper()}")
        # except subprocess.CalledProcessError as e:
        #     messagebox.showerror("Error", f"Failed to convert file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()
