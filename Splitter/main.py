import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def split_video_into_grid(video_path, n_cuts, m_cuts):
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

    # Check if width and height are divisible by n_cuts and m_cuts respectively
    if width % n_cuts != 0:
        messagebox.showerror("Error", f"Width {width} is not divisible by {n_cuts}.")
        return
    if height % m_cuts != 0:
        messagebox.showerror("Error", f"Height {height} is not divisible by {m_cuts}.")
        return

    # Get video file extension
    ext = video_path.split(".")[-1]

    cut_width = width // n_cuts
    cut_height = height // m_cuts

    # Split the video into an n x m grid
    for i in range(n_cuts):
        for j in range(m_cuts):
            output_filename = f"cut_{i + 1}_{j + 1}.{ext}"
            x_offset = i * cut_width
            y_offset = j * cut_height
            filter_str = f"crop={cut_width}:{cut_height}:{x_offset}:{y_offset}"
            command = [
                'ffmpeg', '-i', video_path, '-vf', filter_str, '-c:a', 'copy', output_filename
            ]
            result = subprocess.run(command)
            if result.returncode != 0:
                messagebox.showerror("Error", f"Failed to split video into cut {i + 1}_{j + 1}.")
                return

    messagebox.showinfo("Success", "Video split successfully.")

def select_video_and_split():
    # Open file dialog to select video
    video_path = filedialog.askopenfilename(title="Select a video file",
                                            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
    if not video_path:
        return

    # Prompt the user to enter the number of vertical and horizontal cuts
    n_cuts = simpledialog.askinteger("Input", "Enter the number of vertical cuts:")
    if n_cuts is None or n_cuts <= 0:
        messagebox.showerror("Error", "Invalid number of vertical cuts.")
        return

    m_cuts = simpledialog.askinteger("Input", "Enter the number of horizontal cuts:")
    if m_cuts is None or m_cuts <= 0:
        messagebox.showerror("Error", "Invalid number of horizontal cuts.")
        return

    # Split the video
    split_video_into_grid(video_path, n_cuts, m_cuts)

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
