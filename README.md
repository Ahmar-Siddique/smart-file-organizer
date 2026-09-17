# Smart File Organizer

A Python command-line utility that automatically organizes files into categorized folders based on their file extensions.

# Features

* Organizes files by extension
* Supports Images, Documents, Archives, Videos, Audio, Programs, and Code
* Places unsupported file types into an `Other` folder
* Handles duplicate filenames automatically
* Supports Dry Run mode
* Supports custom folder selection
* Asks for confirmation before organizing files
* Provides organization statistics
* Displays a category summary
* Handles file operation errors without crashing
* Uses a JSON configuration file for file categories
* Maintains an operation log

# Supported Categories

 Category  | Examples                                                   
 --------- | ---------------------------------------------------------- 
 Images    | `.png`, `.jpg`, `.jpeg`, `.gif`                            
 Documents | `.pdf`, `.docx`, `.pptx`, `.txt`, `.csv`                   
 Archives  | `.zip`, `.rar`, `.7z`, `.xz`, `.iso`                       
 Videos    | `.mkv`, `.mp4`, `.avi`, `.mov`, `.webm`                    
 Audio     | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`                    
 Programs  | `.exe`, `.msi`                                             
 Code      | `.py`, `.cpp`, `.c`, `.h`, `.js`, `.html`, `.css`, `.java` 
 Other     | Unsupported file extensions                                

# Project Structure

Smart File Organizer/
│
├── organizer.py
├── config.json
├── organizer.log
└── README.md

## Requirements

* Python 3.10 or newer
* No external Python packages are required.

# How to Run

Open a terminal in the project directory and run:
python organizer.py
The program will ask you to:

1. Select Dry Run or Organize mode.
2. Confirm the organization if using Organize mode.
3. Select the folder to organize.

# Dry Run Mode

Dry Run allows you to preview the changes without actually moving files.

Example:
Would organize photo.png -> Images
Would organize document.pdf -> Documents
Would organize song.mp3 -> Audio
No files are moved while Dry Run is enabled.

# Duplicate Handling

If a file with the same name already exists in the destination folder, the organizer automatically creates a new filename.

For example:
report.pdf
report_1.pdf
report_2.pdf
report_3.pdf
This prevents existing files from being overwritten.

# Example Output

===========================
  Smart File Organizer
===========================
Version :  1.0
Status  : Ready

Mode Selected : Organize

Organizing files....

 photo.png -> Images
 report.pdf -> Documents
   Renamed to report_1.pdf

-----------------------------
Files Scanned   : 3
Files Organized : 3
Duplicates      : 1
Other Files     : 0
Folders Skipped : 2
Files Failed    : 0
-----------------------------

Organization complete.

# Configuration

File categories and their extensions are stored in `config.json`.

Example:

{
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Audio": [".mp3", ".wav", ".flac"]
}

This allows categories and supported extensions to be modified without changing the main Python program

 # Version:

""Version 1.0""

# License

This project is available for educational and personal use.
