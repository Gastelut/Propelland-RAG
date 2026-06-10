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

def list_folder_contents(folder_path):
    """List contents of a folder with recursion level"""
    try:
        result = dbx.files_list_folder(folder_path)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                print(f"[Folder] {entry.path_lower}")
                # Recursively list subfolders
                list_folder_contents(entry.path_lower)
            else:
                print(f"[File]   {entry.path_lower}")
    except Exception as e:
        print(f"Error listing {folder_path}: {e}")

print("=== Contents of 'Sharing for client' ===")
list_folder_contents("/sharing for client")

print("\n=== Contents of 'GC09 Sprint guía de cliente' ===")
list_folder_contents("/gc09 sprint guía de cliente")
