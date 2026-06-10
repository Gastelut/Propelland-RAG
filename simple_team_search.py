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
    print("=== Searching for team folder patterns ===")
    
    # Try to find any folder that might contain the company structure
    patterns = [
        "Propelland",
        "Shared",
        "Team Folder",
        "Team Space"
    ]
    
    for pattern in patterns:
        try:
            result = dbx.files_search("", pattern, max_results=3)
            for match in result.matches:
                entry = match.metadata
                if isinstance(entry, files.FolderMetadata):
                    print(f"\nFound: {entry.name}")
                    print(f"Path: {entry.path_lower}")
                    
                    try:
                        # List first 5 entries
                        contents = dbx.files_list_folder(entry.path_lower, recursive=False)
                        print(f"Contents ({len(contents.entries)} items):")
                        for i, sub_entry in enumerate(contents.entries[:5]):
                            if isinstance(sub_entry, files.FolderMetadata):
                                print(f"  {i+1}. [Folder] {sub_entry.name}")
                            else:
                                print(f"  {i+1}. [File] {sub_entry.name}")
                        
                        if len(contents.entries) > 5:
                            print(f"  ... and {len(contents.entries) - 5} more")
                            
                    except Exception as e:
                        print(f"Error listing contents: {e}")
                        
        except Exception as e:
            print(f"\nError searching for '{pattern}': {e}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    print(traceback.format_exc())
