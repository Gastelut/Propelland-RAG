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
    print("=== Personal Root Folder Contents ===")
    
    # List root directory
    root_result = dbx.files_list_folder("", recursive=False)
    
    print(f"Root has {len(root_result.entries)} entries")
    
    # Group by file type
    folders = []
    files_list = []
    
    for entry in root_result.entries:
        if isinstance(entry, files.FolderMetadata):
            folders.append(entry)
        else:
            files_list.append(entry)
            
    print(f"Folders: {len(folders)}")
    print(f"Files: {len(files_list)}")
    
    print("\n=== Folder List ===")
    for folder in sorted(folders, key=lambda x: x.name.lower()):
        print(f"  - {folder.name}")
        
        # Check if this might contain Propelland folders
        if "propelland" in folder.name.lower() or "shared" in folder.name.lower():
            try:
                subcontents = dbx.files_list_folder(folder.path_lower, recursive=False)
                print(f"    Contains {len(subcontents.entries)} items")
                for sub_entry in subcontents.entries[:5]:
                    if isinstance(sub_entry, files.FolderMetadata):
                        print(f"      [Folder] {sub_entry.name}")
                    else:
                        print(f"      [File] {sub_entry.name}")
                if len(subcontents.entries) > 5:
                    print(f"      ... and {len(subcontents.entries) - 5} more")
            except Exception as e:
                print(f"    Error listing contents: {e}")
                
except Exception as e:
    print(f"Error checking root: {e}")
    import traceback
    print(traceback.format_exc())
