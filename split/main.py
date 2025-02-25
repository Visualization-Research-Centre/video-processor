import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def split_video_into_grid(video_path, output_dir, n_cuts, m_cuts):
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

    # Get video file name and extension
    ext = video_path.split(".")[-1]
    vname = os.path.basename(video_path).split(".")[0]

    cut_width = width // n_cuts
    cut_height = height // m_cuts

    # Split the video into an n x m grid
    for i in range(n_cuts):
        for j in range(m_cuts):
            output_filename = f"{vname}_cut_{i + 1}_{j + 1}.{ext}"
            output_filename = os.path.join(output_dir, output_filename)
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

def browse_video(video_path_entry):
    video_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
    )
    if video_path:
        video_path_entry.delete(0, tk.END)
        video_path_entry.insert(0, video_path)

def browse_output_dir(output_dir_entry):
    output_dir = filedialog.askdirectory(title="Select an output directory")
    if output_dir:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, output_dir)

def select_video_and_split(video_path_entry, output_dir_entry, n_cuts_entry, m_cuts_entry):
    video_path = video_path_entry.get()
    output_dir = output_dir_entry.get()
    try:
        n_cuts = int(n_cuts_entry.get())
        m_cuts = int(m_cuts_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Number of cuts must be integers.")
        return

    if not video_path or not output_dir or n_cuts <= 0 or m_cuts <= 0:
        messagebox.showerror("Error", "All fields must be filled with valid data.")
        return

    # make sure the output dir exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Split the video
    split_video_into_grid(video_path, output_dir, n_cuts, m_cuts)

def main():
    # Set up the main application window
    root = tk.Tk()
    root.title("Video Splitter")

    # Video path entry
    tk.Label(root, text="Video Path:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    video_path_entry = tk.Entry(root, width=50)
    video_path_entry.grid(row=0, column=1, padx=10, pady=5)
    video_browse_button = tk.Button(root, text="Browse", command=lambda: browse_video(video_path_entry))
    video_browse_button.grid(row=0, column=2, padx=5, pady=5)

    # Output directory entry
    tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    output_dir_entry = tk.Entry(root, width=50)
    output_dir_entry.grid(row=1, column=1, padx=10, pady=5)
    output_browse_button = tk.Button(root, text="Browse", command=lambda: browse_output_dir(output_dir_entry))
    output_browse_button.grid(row=1, column=2, padx=5, pady=5)

    # Number of vertical cuts entry
    tk.Label(root, text="Vertical Cuts:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    n_cuts_entry = tk.Entry(root, width=10)
    n_cuts_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

    # Number of horizontal cuts entry
    tk.Label(root, text="Horizontal Cuts:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    m_cuts_entry = tk.Entry(root, width=10)
    m_cuts_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

    # Create a button to process the video
    process_button = tk.Button(root, text="Process", command=lambda: select_video_and_split(video_path_entry, output_dir_entry, n_cuts_entry, m_cuts_entry))
    process_button.grid(row=4, column=0, columnspan=3, pady=20)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
