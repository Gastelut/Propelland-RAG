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
    print("=== Searching for client projects ===")
    
    # Search for client projects
    search_result = dbx.files_search("", "Client Projects", max_results=10)
    print(f"\nFound {len(search_result.matches)} matches for 'Client Projects'")
    
    for i, match in enumerate(search_result.matches):
        entry = match.metadata
        if isinstance(entry, files.FolderMetadata):
            print(f"\nMatch {i+1}: {entry.name}")
            print(f"Path: {entry.path_lower}")
            
            # List contents
            contents = dbx.files_list_folder(entry.path_lower, recursive=False)
            print(f"Contents ({len(contents.entries)} items):")
            for j, sub_entry in enumerate(contents.entries[:10]):
                if isinstance(sub_entry, files.FolderMetadata):
                    print(f"  {j+1}. [Folder] {sub_entry.name}")
                else:
                    print(f"  {j+1}. [File] {sub_entry.name}")
                    
            if len(contents.entries) > 10:
                print(f"  ... and {len(contents.entries) - 10} more")
                
except Exception as e:
    print(f"Error searching for client projects: {e}")
    import traceback
    print(traceback.format_exc())
