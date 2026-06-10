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

# Check for client projects or business development folders
print("=== Checking for Client Projects and Business Development folders ===")

# Check if there's a folder that might contain client projects
for entry in dbx.files_list_folder("").entries:
    if isinstance(entry, dropbox.files.FolderMetadata) and any(keyword in entry.name.lower() for keyword in ['client', 'project', 'business', 'development']):
        print(f"\nFound potential relevant folder: {entry.name}")
        list_folder_contents(entry.path_lower)

print("\n=== Complete list of all folders ===")
for entry in dbx.files_list_folder("", recursive=True).entries:
    if isinstance(entry, dropbox.files.FolderMetadata):
        print(entry.path_lower)
