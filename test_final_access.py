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
    print("=== Testing team space access ===")
    
    # Get account info
    account_info = dbx.users_get_current_account()
    print(f"Account: {account_info.name.display_name}")
    print(f"Team: {account_info.team.name}")
    
    # List root directory to see if company folders are now visible
    print("\n=== Root Directory Contents ===")
    result = dbx.files_list_folder("", recursive=False)
    
    print(f"Total entries: {len(result.entries)}")
    
    # Check for company folders
    company_folders = []
    for entry in result.entries:
        if isinstance(entry, files.FolderMetadata):
            if entry.name.startswith("01") or entry.name.startswith("02") or entry.name.startswith("03"):
                company_folders.append(entry.name)
                
    print(f"Company folders found: {len(company_folders)}")
    
    if company_folders:
        print("\n=== Company Folders ===")
        for folder in sorted(company_folders):
            print(f"  ✓ {folder}")
            
        # Verify we can access one of these folders
        first_folder = company_folders[0]
        try:
            folder_path = f"/{first_folder}"
            folder_content = dbx.files_list_folder(folder_path, recursive=False)
            print(f"\nContents of '{first_folder}' ({len(folder_content.entries)} items):")
            
            subfolders = []
            files_count = 0
            
            for entry in folder_content.entries:
                if isinstance(entry, files.FolderMetadata):
                    subfolders.append(entry.name)
                else:
                    files_count += 1
                    
            print(f"  Subfolders: {len(subfolders)}")
            print(f"  Files: {files_count}")
            
            if subfolders:
                print("  Top subfolders:")
                for subfolder in sorted(subfolders)[:5]:
                    print(f"    - {subfolder}")
                    
        except Exception as e:
            print(f"Error accessing '{first_folder}': {e}")
            
    else:
        print("\n❌ No company folders found at root")
        
        # Show what folders are actually visible
        print("\n=== Visible Folders ===")
        folders = [entry.name for entry in result.entries if isinstance(entry, files.FolderMetadata)]
        for folder in sorted(folders):
            print(f"  - {folder}")
            
except Exception as e:
    print(f"Error testing access: {e}")
    import traceback
    print(traceback.format_exc())
