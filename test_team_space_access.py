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
    
    # Try to get account info
    account_info = dbx.users_get_current_account()
    print(f"Account: {account_info.name.display_name}")
    print(f"Team: {account_info.team.name}")
    print(f"Root namespace: {account_info.root_info.root_namespace_id}")
    
    # Look for the Propelland team folder specifically
    print("\n=== Looking for Propelland Team Folder ===")
    
    # Search for team folder variations
    team_folder_patterns = [
        "Propelland Team Folder",
        "Propelland Team folder",
        "Propelland team folder",
        "Propelland Shared",
        "Company Folder"
    ]
    
    found_team_folders = []
    for pattern in team_folder_patterns:
        try:
            result = dbx.files_search("", pattern, max_results=3)
            for match in result.matches:
                entry = match.metadata
                if isinstance(entry, files.FolderMetadata):
                    print(f"\nFound: {entry.name} ({entry.path_lower})")
                    found_team_folders.append(entry.path_lower)
                    
                    # List contents
                    contents = dbx.files_list_folder(entry.path_lower, recursive=False)
                    print(f"Contents ({len(contents.entries)} items):")
                    for sub_entry in contents.entries:
                        if isinstance(sub_entry, files.FolderMetadata):
                            print(f"  [Folder] {sub_entry.name}")
                        else:
                            print(f"  [File] {sub_entry.name}")
                            
        except Exception as e:
            print(f"Error searching for '{pattern}': {e}")
            
    # Try to access team root directly if available
    print("\n=== Trying team space endpoints ===")
    
    try:
        # This is how you access team space in Dropbox Business
        # It might be in a specific namespace or path
        print("\nChecking if team space is accessible at /team")
        result = dbx.files_list_folder("/team", recursive=False)
        print(f"Team space at /team has {len(result.entries)} entries")
        for entry in result.entries:
            if isinstance(entry, files.FolderMetadata):
                print(f"  [Folder] {entry.name}")
                
    except Exception as e:
        print(f"Error accessing /team: {e}")
        
    try:
        print("\nChecking if team space is accessible at /")
        # We already checked this, but let's re-list to confirm
        result = dbx.files_list_folder("", recursive=False)
        print(f"Root has {len(result.entries)} entries")
        folders = [entry for entry in result.entries if isinstance(entry, files.FolderMetadata)]
        print(f"Top-level folders: {len(folders)}")
        
        # Check if any of these folders look like company folders
        company_folders_found = 0
        for folder in folders:
            if folder.name.startswith("01") or folder.name.startswith("02") or folder.name.startswith("03"):
                print(f"  ✓ Found company folder: {folder.name}")
                company_folders_found += 1
                
        print(f"\nCompany folders found at root: {company_folders_found}")
                
    except Exception as e:
        print(f"Error accessing root: {e}")
        
    print("\n=== Summary ===")
    if found_team_folders:
        print(f"Found {len(found_team_folders)} team folder(s):")
        for path in found_team_folders:
            print(f"  - {path}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    print(traceback.format_exc())
