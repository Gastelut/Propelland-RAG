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

def search_all_namespaces():
    """Try to find the team root folders by searching for known patterns"""
    # Search patterns based on the local Dropbox structure
    search_patterns = [
        "01 Client Projects",
        "02 Business Development",
        "03 Propelland Brand",
        "04 Competitive",
        "05 Team",
        "06 Tools",
        "07 Events",
        "08 Propel U",
        "09 Propel Org",
        "10 Propel Labs",
        "11 Admin"
    ]
    
    print("=== Searching for team root folders ===")
    
    for pattern in search_patterns:
        try:
            result = dbx.files_search("", pattern, max_results=50)
            if result.matches:
                print(f"\n=== Results for '{pattern}' ===")
                for match in result.matches:
                    entry = match.metadata
                    if hasattr(entry, 'path_lower'):
                        print(f"  {entry.path_lower}")
        except Exception as e:
            print(f"\nError searching for '{pattern}': {e}")

# Try to get team folder info from shared folders
def list_shared_folders():
    print("\n=== Shared Folders ===")
    try:
        result = dbx.sharing_list_folders()
        if result.folders:
            for folder in result.folders:
                print(f"[Shared Folder] {folder.name} ({folder.path_lower})")
        else:
            print("No shared folders found")
    except Exception as e:
        print(f"Error listing shared folders: {e}")
        import traceback
        print(traceback.format_exc())

search_all_namespaces()
list_shared_folders()
