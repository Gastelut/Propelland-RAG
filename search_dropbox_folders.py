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

def search_for_folders(keyword):
    """Search for folders containing the keyword"""
    try:
        # Search the entire Dropbox for folders containing the keyword
        result = dbx.files_search("", keyword, max_results=100)
        print(f"\n=== Search results for '{keyword}' ===")
        for match in result.matches:
            entry = match.metadata
            if isinstance(entry, dropbox.files.FolderMetadata):
                print(f"[Folder] {entry.path_lower}")
            else:
                print(f"[File] {entry.path_lower}")
                
        if not result.matches:
            print(f"No results found for '{keyword}'")
            
    except Exception as e:
        print(f"Error searching for '{keyword}': {e}")

# Search for relevant folders
search_for_folders("Client Projects")
search_for_folders("01 Client")
search_for_folders("Business Development")
search_for_folders("02 Business")

print("\n=== Search complete ===")
