import os
from dotenv import load_dotenv
import dropbox

# Load environment variables
load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    raise SystemExit("DROPBOX_ACCESS_TOKEN missing in .env")

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

try:
    # List root directory
    result = dbx.files_list_folder("")
    print("Root directory contents:")
    for entry in result.entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            print(f"[Folder] {entry.name}")
    
    print("\n=== End of root directory list ===")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    print(traceback.format_exc())
