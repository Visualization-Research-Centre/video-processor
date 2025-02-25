
# Video Processing Tools

a simple collection of video-processing tools:
- encode/: UI to choose encoder and format
- split: UI to split a video into a grid


### Requirements
- ffmpeg
- python


### Windows
#### Setup
##### choco
First install chocolatey: open powershell in admin mode
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```


##### verify ffmpeg
Then install ffmpeg
```powershell
choco install ffmpeg
```
open a new powershell (not admin):
```powershell
ffmpeg
```

##### Install python
Open powershell (not admin):
```powershell
python3.exe
```

This will open MS store where you can install python from

#### Usage
Open powershell and go to this folder. Go into Splitter.
```powershell
python main.py
```

The tool should be self-explanatory.

