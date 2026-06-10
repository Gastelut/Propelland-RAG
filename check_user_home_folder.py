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
    print("=== Checking for user-specific folders ===")
    
    # Check if there's a folder with your name or "home" in the root
    root_result = dbx.files_list_folder("", recursive=False)
    
    user_folders = []
    for entry in root_result.entries:
        if isinstance(entry, files.FolderMetadata):
            # Look for folders that might contain user-specific content
            folder_name = entry.name.lower()
            if "esteban" in folder_name or "gastelut" in folder_name or "home" in folder_name:
                user_folders.append(entry)
                
    if user_folders:
        print(f"Found {len(user_folders)} user-specific folders:")
        for folder in user_folders:
            print(f"\n[Folder] {folder.name} ({folder.path_lower})")
            # List contents
            try:
                contents = dbx.files_list_folder(folder.path_lower, recursive=False)
                print("  Contents:")
                for sub_entry in contents.entries:
                    if isinstance(sub_entry, files.FolderMetadata):
                        print(f"    [Folder] {sub_entry.name}")
                    else:
                        print(f"    [File] {sub_entry.name}")
                        
            except Exception as e:
                print(f"  Error listing contents: {e}")
    else:
        print("No user-specific folders found in root")
        
except Exception as e:
    print(f"Error checking user folders: {e}")
    import traceback
    print(traceback.format_exc())
