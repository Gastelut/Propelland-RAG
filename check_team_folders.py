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
    # Check team folder info
    print("=== Checking Team Folders ===")
    
    # Get current account info
    account_info = dbx.users_get_current_account()
    
    # Try to list team root namespace contents
    print("\n--- Root namespace contents ---")
    result = dbx.files_list_folder("", recursive=False)
    print(f"Folders found in root: {len([entry for entry in result.entries if isinstance(entry, files.FolderMetadata)])}")
    for entry in result.entries:
        if isinstance(entry, files.FolderMetadata):
            print(f"[Folder] {entry.name} ({entry.path_lower})")
    
    # Try to check namespace info
    print("\n--- Namespace Info ---")
    namespaces = dbx.users_list_namespaces()
    print(f"Number of namespaces: {len(namespaces.namespaces)}")
    for ns in namespaces.namespaces:
        print(f"\nNamespace ID: {ns.namespace_id}")
        print(f"Name: {ns.name}")
        print(f"Type: {ns.namespace_type}")
        
        try:
            print(f"Contents of {ns.name}:")
            # List root of this namespace
            result = dbx.files_list_folder("", recursive=False, include_non_downloadable_files=False, team_member_id=None)
            folder_count = len([entry for entry in result.entries if isinstance(entry, files.FolderMetadata)])
            print(f"  Folders: {folder_count}")
            for entry in result.entries:
                if isinstance(entry, files.FolderMetadata):
                    print(f"  [Folder] {entry.name}")
        except Exception as e:
            print(f"  Error listing contents: {e}")
            
except Exception as e:
    print(f"Error checking team folders: {e}")
    import traceback
    print(traceback.format_exc())
