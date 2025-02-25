import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def split_video_vertically(video_path, n_cuts):
    # Get video dimensions using FFmpeg
    command = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=width,height', '-of', 'default=noprint_wrappers=1:nokey=1', video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        messagebox.showerror("Error", "Failed to get video dimensions.")
        return

    width, height = map(int, result.stdout.decode().strip().split())

    # Check if width is divisible by n_cuts
    if width % n_cuts != 0:
        messagebox.showerror("Error", f"Width {width} is not divisible by {n_cuts}.")
        return
    
    # get video_path extension
    ext = video_path.split(".")[-1]

    cut_width = width // n_cuts

    # Split the video into vertical cuts
    for i in range(n_cuts):
        output_filename = f"cut_{i + 1}.{ext}"
        x_offset = i * cut_width
        filter_str = f"crop={cut_width}:{height}:{x_offset}:0"
        command = [
            'ffmpeg', '-i', video_path, '-vf', filter_str, '-c:a', 'copy', output_filename
        ]
        result = subprocess.run(command)
        if result.returncode != 0:
            messagebox.showerror("Error", f"Failed to split video into cut {i + 1}.")
            return

    messagebox.showinfo("Success", "Video split successfully.")

def select_video_and_split():
    # Open file dialog to select video
    video_path = filedialog.askopenfilename(title="Select a video file",
                                            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
    if not video_path:
        return

    # Prompt the user to enter the number of cuts
    n_cuts = simpledialog.askinteger("Input", "Enter the number of vertical cuts:")
    
    if n_cuts is None or n_cuts <= 0:
        messagebox.showerror("Error", "Invalid number of cuts.")
        return

    # Split the video
    split_video_vertically(video_path, n_cuts)

def main():
    # Set up the main application window
    root = tk.Tk()
    root.title("Video Splitter")

    # Create a button to select the video file
    select_button = tk.Button(root, text="Select Video and Split", command=select_video_and_split)
    select_button.pack(pady=20)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
