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
    print("=== Detailed Root Folder Listing ===")
    print("====================================")
    
    # List root directory
    root_result = dbx.files_list_folder("", recursive=False)
    
    print(f"Total entries at root: {len(root_result.entries)}")
    print()
    
    folders = [entry for entry in root_result.entries if isinstance(entry, files.FolderMetadata)]
    files_list = [entry for entry in root_result.entries if not isinstance(entry, files.FolderMetadata)]
    
    print(f"Folders ({len(folders)}):")
    for i, folder in enumerate(sorted(folders, key=lambda x: x.name.lower())):
        try:
            # Check if we can access this folder's contents
            sub_result = dbx.files_list_folder(folder.path_lower, recursive=False)
            sub_folders = [e for e in sub_result.entries if isinstance(e, files.FolderMetadata)]
            sub_files = [e for e in sub_result.entries if not isinstance(e, files.FolderMetadata)]
            
            print(f"{i+1}. {folder.name}")
            print(f"   Path: {folder.path_lower}")
            print(f"   Contents: {len(sub_folders)} folders, {len(sub_files)} files")
            
            # Show first 3 subfolders if any
            if sub_folders:
                print(f"   Subfolders: {', '.join([sf.name for sf in sub_folders[:3]])}{'...' if len(sub_folders) > 3 else ''}")
                
            print()
            
        except Exception as e:
            print(f"{i+1}. {folder.name} - Error: {e}")
            print()
            
    print("=" * 50)
    print(f"Files ({len(files_list)}):")
    for i, file in enumerate(sorted(files_list, key=lambda x: x.name.lower())):
        print(f"{i+1}. {file.name}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    print(traceback.format_exc())
