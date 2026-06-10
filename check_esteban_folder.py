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
    # Look for folders containing Esteban Gastelut or similar
    print("=== Searching for Esteban's folders ===")
    
    # Search for folders with Esteban in the name
    search_result = dbx.files_search("", "Esteban", max_results=20)
    for match in search_result.matches:
        entry = match.metadata
        if isinstance(entry, files.FolderMetadata):
            print(f"[Folder] {entry.name} ({entry.path_lower})")
            
            # List contents of this folder
            try:
                folder_contents = dbx.files_list_folder(entry.path_lower, recursive=False)
                print("  Contents:")
                for sub_entry in folder_contents.entries:
                    if isinstance(sub_entry, files.FolderMetadata):
                        print(f"    [Folder] {sub_entry.name}")
                    else:
                        print(f"    [File] {sub_entry.name}")
                        
                print()
            except Exception as e:
                print(f"  Error listing contents: {e}")
                
except Exception as e:
    print(f"Error searching for Esteban's folders: {e}")
    import traceback
    print(traceback.format_exc())
