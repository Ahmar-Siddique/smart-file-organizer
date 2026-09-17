from pathlib import Path
from datetime import datetime
import json
def validate_categories(categories):
    if not isinstance(categories,dict):
        print("Error: Category must be a JSON object")
        return False
    for category,extensions in categories.items():
        if not isinstance(category,str):
            print("Error: Category must be a string. ")
            return False
        if not isinstance(extensions,list):
                    print("Error: Extensions must be a list. ")
                    return False
        for extension in extensions:
            if not isinstance(extension,str):
                print(f"Extensions in {category} must be strings")
                return False
        for extension in extensions:
            if not extension.startswith("."):
                print(f"Invalid syntax '{extension}' in '{category}'. ")
                return False
    return True
def load_categories():
    config_files=Path(__file__).parent/"config.json"
    try:
        with open(config_files,"r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: cofig.json was not found")
        print("Creating config.json file with default configuration")
        try:
            with open(config_files,"w",encoding="utf-8") as file:
                json.dump(categories,file,indent=4)
            print("Default config.json created")
            return categories
        except OSError as error:
            print(f"Could not create config.json due to {error} ")
            return None
    except json.JSONDecodeError:
        print("Error: config.json contains invalid json")
        return None
def get_default_categories():
    return {
        "Images": [".png", ".jpg", ".jpeg", ".gif"],
        "Documents": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".txt", ".csv", ".md"],
        "Archives": [".zip", ".rar", ".7z", ".xz", ".iso", ".dmg"],
        "Videos": [".mkv", ".mp4", ".avi", ".mov", ".webm", ".m4v", ".mpeg", ".mpg"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Programs": [".exe", ".msi"],
        "Code": [".py", ".cpp", ".c", ".h", ".hpp", ".js", ".html", ".css", ".java"]
    }
VERSION = "1.0"
def determine_category(extension):
    folder="Other"
    for category,extensions in categories.items():
        if extension.lower() in extensions:
            folder=category
            break
    return folder
def get_destination_folder(downloads,folder,dry_run):
    destination=downloads/folder
    if not destination.exists() and not dry_run:
        destination.mkdir()
    return destination
def move_file(item,destination,dry_run):
    new_location= destination/item.name
    duplicate = False
    if new_location.exists():
        duplicate = True
        counter=1
        while new_location.exists():
            new_name=f"{item.stem}_{counter}{item.suffix}"
            new_location=destination/new_name
            if not new_location.exists():
                break
            counter+=1
    success=False
    error_msg=None
    if dry_run:
        success=True
    else:
        try:
            item.rename(new_location)
            success=True
        except OSError as error:
            error_msg=str(error)
    return new_location,duplicate,success,error_msg
def choose_mode():
    print()
    print("----Select mode----")
    print("1. DRY RUN ")
    print("2. Organize files")
    while True:
        try:
            choice=int(input("Enter your choice : "))
            if choice == 1:
                return True
            elif choice==2 :
                return False
            else:
                print("Invalid choice! Please enter 1 or 2.")
        except ValueError:
            print("Invalid input! Please enter a number.")
def print_summary(files_scanned, files_organized, duplicates, other_files, folders_skipped,files_failed):
    print("-----------------------------")       
    print(f"Files Scanned   : {files_scanned}")
    print(f"Files Organized : {files_organized}")
    print(f"Duplicates      : {duplicates}") 
    print(f"Other Files     : {other_files}")
    print(f"Folders/files Skipped : {folders_skipped}")
    print(f"Files Failed    : {files_failed}")
    print("-----------------------------")
def print_category_summary(category_counts):
    if not category_counts:
        print("No categories to display")
        print("--------------------------")
        return
    print()
    print("Category Summary")
    print("-----------------------------")
    for category,counts in category_counts.items():
        print(f"{category:<15}: {counts}")
    print("----------------------------")

def confirm_organization():
    print()
    print("Are you sure you want to organize these files?")
    print("1. Yes")
    print("2. No")
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                return True
            elif choice == 2:
                return False
            else:
                print("Invalid choice! Please enter 1 or 2.")
        except ValueError:
            print("Invalid input! Please enter a number.") 
def choose_path():
    print()
    print("------Select Folder-----")
    print("1. Downloads")
    print("2. Choose custom path")
    while True:
        try:
            choice=int(input("Enter your choice: "))
            if choice==1:
                folder=Path.home()/"Downloads"
                if not folder.exists():
                    print("Downloads folder doesn't exists. ")
                    print("Choose another folder. ")
                    continue
                return Path(folder)
            elif choice==2:
                folder=Path(input("Enter folder path :").strip())
                if not folder.exists():
                    print("Folder doesn't exists.Please try again.")
                elif not folder.is_dir():
                    print("The selected path is not a folder.")
                else:
                    return Path(folder)
            else:
                print("Invalid choice! Please enter 1 or 2.")
        except ValueError:
            print("Invalid Input! Please enter a number")
def print_header():
        print("===========================")
        print("  Smart File Organizer   ")
        print("===========================")
        print("Version : ",VERSION)
        print("Status  : Ready ")
def organization(downloads,DRY_RUN,log_file):
        files_scanned = 0
        files_organized = 0
        duplicates =0
        other_files=0
        folders_skipped=0
        files_failed=0
        category_counts={}
        for item in downloads.iterdir():
            Skip_files={"organizer.log","config.json","README.md","organizer.py"}
            if item.name in Skip_files:
                folders_skipped+=1
                continue
            if item.is_file():
                files_scanned+=1
                folder=determine_category(item.suffix)
                category_counts[folder]=category_counts.get(folder,0)+1
                if folder=="Other":
                    other_files+=1
                destination = get_destination_folder(downloads,folder,DRY_RUN)
                new_location,duplicate,success,error_msg = move_file(item, destination,DRY_RUN)
                if success:
                    if DRY_RUN:
                        print(f"Would organize {item.name} -> {folder}")
                        write_log(log_file,item,new_location,"DRY_RUN")
                    else:
                        files_organized+=1
                        print(f" {item.name} -> {folder}")
                        if duplicate:
                            duplicates+=1
                            print(f"   Renamed to {new_location.name}")
                        status = "DUPLICATE" if duplicate else "SUCCESS"
                        write_log(log_file, item, new_location, status)
                else:
                    files_failed+=1
                    print(f" Could not organize {item.name}")
                    print(f"   Reason: {error_msg}") 
                    write_log(log_file, item, destination, f"FAILED: {error_msg}")  
            elif item.is_dir():
                folders_skipped+=1
        print_summary(files_scanned, files_organized,duplicates,other_files,folders_skipped,files_failed)
        print_category_summary(category_counts)
def write_log(log_file, item, destination, status):
    timestamp = datetime.now().strftime("%Y-%m-%d || %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(
            f"{timestamp} | {item.name} | {destination} | {status}\n"
        )
def main():
    global categories
    categories=load_categories()
    if categories is None:
        return
    if not validate_categories(categories):
        return
    print_header()

    DRY_RUN=choose_mode()
    if not DRY_RUN:
        confirmed=confirm_organization()
        if not confirmed:
            print("Organization cancelled. ")
            return
    if DRY_RUN:
        print()
        print("Mode Selected : Dry Run ")
    else:
        print("Mode Selected : Organize")
        print()
        print("Organizing files....")
    print()
    downloads=choose_path()
    print(f"Selected folder: {downloads}")
    log_file = Path(__file__).parent / "organizer.log"
    organization(downloads,DRY_RUN, log_file)

    if DRY_RUN:
        print("Dry run completed, no files were moved.")
    else:  
        print("Organization complete.")
if __name__ == "__main__":
   main()