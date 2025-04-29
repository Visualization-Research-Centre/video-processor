import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re
import subprocess

class ImageSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sequence Splitter")
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.start_index = tk.IntVar(value=1)
        self.num_cuts = tk.IntVar(value=6)
        self.input_pattern = ""
        self.input_directory = ""

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Input File Selection
        ttk.Label(self.root, text="Input Image:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.root, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)

        # Output Directory Selection
        ttk.Label(self.root, text="Output Directory:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.root, textvariable=self.output_dir, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)

        # Start Index
        ttk.Label(self.root, text="Start Index:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.root, textvariable=self.start_index).grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Number of Cuts
        ttk.Label(self.root, text="Vertical Cuts:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        ttk.Spinbox(self.root, from_=1, to=20, textvariable=self.num_cuts).grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        # Parallel Processing Option
        self.parallel_var = tk.BooleanVar()
        ttk.Checkbutton(self.root, text="Process in Parallel", variable=self.parallel_var).grid(row=4, column=1, padx=5, pady=5, sticky='w')
        

        # Process Button
        ttk.Button(self.root, text="Process", command=self.process).grid(row=5, column=1, padx=5, pady=10)
        

    def browse_input(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.input_path.set(filename)
            self.parse_input_pattern(filename)

    def parse_input_pattern(self, filename):
        base_name = os.path.basename(filename)
        matches = list(re.finditer(r'\d+', base_name))
        
        if not matches:
            messagebox.showerror("Error", "No numeric sequence found in filename")
            return
            
        last_match = matches[-1]
        num_digits = len(last_match.group())
        self.input_pattern = (base_name[:last_match.start()] + 
                             f"%0{num_digits}d" + 
                             base_name[last_match.end():])
        self.input_directory = os.path.dirname(filename)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def process(self):
        if not self.validate_inputs():
            return

        for i in range(self.num_cuts.get()):
            output_dir = os.path.join(self.output_dir.get(), f"C{i+1}")
            os.makedirs(output_dir, exist_ok=True)
            
            cmd = [
                'ffmpeg',
                '-start_number', str(self.start_index.get()),
                '-i', os.path.join(self.input_directory, self.input_pattern),
                '-vf', f'crop=iw/{self.num_cuts.get()}:ih:iw/{self.num_cuts.get()}*{i}:0',
                '-q:v', '1',
                '-qmin', '1',
                '-qmax', '1',
                os.path.join(output_dir, self.input_pattern)
            ]

            try:
                if self.parallel_var.get():
                    subprocess.Popen(cmd)
                else:
                    subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to process cut {i+1}:\n{e}")
                return

        messagebox.showinfo("Success", "All cuts processed successfully!")

    def validate_inputs(self):
        if not self.input_directory or not self.input_pattern:
            messagebox.showerror("Error", "Please select a valid input image")
            return False
        if not self.output_dir.get():
            messagebox.showerror("Error", "Please select an output directory")
            return False
        if self.num_cuts.get() < 1:
            messagebox.showerror("Error", "Number of cuts must be at least 1")
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSplitterApp(root)
    root.mainloop()
