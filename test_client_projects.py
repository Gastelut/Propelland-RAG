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
    print("=== Testing if '01 Client Projects' exists ===")
    
    # Try different path variations
    test_paths = [
        "/01 Client Projects",
        "/01 client projects",
        "01 Client Projects",
        "/01 Client Projects/",
        "01 client projects"
    ]
    
    for path in test_paths:
        try:
            # Try to get metadata for the folder
            metadata = dbx.files_get_metadata(path)
            if isinstance(metadata, files.FolderMetadata):
                print(f"✓ Folder exists at: {metadata.path_lower}")
                
                # List contents if we find it
                print(f"Contents of '{path}':")
                contents = dbx.files_list_folder(metadata.path_lower, recursive=False)
                for entry in contents.entries:
                    if isinstance(entry, files.FolderMetadata):
                        print(f"  [Folder] {entry.name}")
                    else:
                        print(f"  [File] {entry.name}")
                
                print()
                
        except Exception as e:
            print(f"✗ Path '{path}' not found: {e}")
            
except Exception as e:
    print(f"Error testing paths: {e}")
    import traceback
    print(traceback.format_exc())
