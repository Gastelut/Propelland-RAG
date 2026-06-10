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
    print("=== Checking 'one global team' folders ===")
    
    # Search for all "one global team" folders
    search_result = dbx.files_search("", "one global team", max_results=10)
    print(f"Found {len(search_result.matches)} 'one global team' folders")
    
    for match in search_result.matches:
        entry = match.metadata
        if isinstance(entry, files.FolderMetadata):
            print(f"\n=== {entry.name} ({entry.path_lower}) ===")
            
            # List immediate contents
            try:
                contents = dbx.files_list_folder(entry.path_lower, recursive=False)
                for sub_entry in contents.entries:
                    if isinstance(sub_entry, files.FolderMetadata):
                        print(f"[Folder] {sub_entry.name}")
                        
            except Exception as e:
                print(f"Error listing contents: {e}")
                
except Exception as e:
    print(f"Error checking 'one global team' folders: {e}")
    import traceback
    print(traceback.format_exc())
