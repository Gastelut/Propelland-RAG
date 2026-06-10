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
    # Check API version and capabilities
    print("=== API Information ===")
    print(f"Dropbox SDK version: {dropbox.__version__}")
    
    # Get account info
    account_info = dbx.users_get_current_account()
    
    print("\n=== Account Info ===")
    print(f"Name: {account_info.name.display_name}")
    print(f"Email: {account_info.email}")
    print(f"Account type: {account_info.account_type}")
    
    if hasattr(account_info, 'team'):
        print(f"\nTeam: {account_info.team.name}")
        
    # Check root namespace
    print(f"\nRoot namespace ID: {account_info.root_info.root_namespace_id}")
    
    # Try to list the root with different parameters
    print("\n=== Root folder contents ===")
    
    # Try with include_deleted=False
    result = dbx.files_list_folder("", recursive=False, include_deleted=False)
    print(f"Files and folders in root: {len(result.entries)}")
    
    folders = []
    files_list = []
    
    for entry in result.entries:
        if isinstance(entry, files.FolderMetadata):
            folders.append(entry.name)
        else:
            files_list.append(entry.name)
    
    print(f"Folders: {len(folders)}")
    print(f"Files: {len(files_list)}")
    
    print("\nFirst 20 folder names:")
    for folder in sorted(folders)[:20]:
        print(f"  - {folder}")
        
except Exception as e:
    print(f"Error checking business info: {e}")
    import traceback
    print(traceback.format_exc())
