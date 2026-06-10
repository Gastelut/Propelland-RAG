import os
from dotenv import load_dotenv
import dropbox
from dropbox import files

# Load environment variables
load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    raise SystemExit("DROPBOX_ACCESS_TOKEN missing in .env")

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

try:
    folder_path = "/jorge alvarez�s files/shared/paula vega home content/folder org"
    
    print("=== Checking contents of: folder org ===")
    result = dbx.files_list_folder(folder_path, recursive=False)
    
    for entry in result.entries:
        if isinstance(entry, files.FolderMetadata):
            print(f"[Folder] {entry.name}")
        else:
            print(f"[File] {entry.name}")
            
    # Check if this is indeed the correct folder by looking for expected subfolders
    expected_folders = ["01 Client Projects", "02 Business Development", "03 Propelland Brand"]
    found = []
    for entry in result.entries:
        if isinstance(entry, files.FolderMetadata):
            if entry.name in expected_folders:
                found.append(entry.name)
                
    print(f"\nFound expected folders: {len(found)}/{len(expected_folders)}")
    for folder in found:
        print(f"  ✓ {folder}")
        
except Exception as e:
    print(f"Error checking folder: {e}")
    import traceback
    print(traceback.format_exc())
