import os
from dotenv import load_dotenv
import dropbox
import requests

# Load environment variables
load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    raise SystemExit("DROPBOX_ACCESS_TOKEN missing in .env")

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def check_api_availability():
    print("=== Checking API Endpoint Availability ===")
    
    endpoints = {
        "users_get_current_account": dbx.users_get_current_account,
        "files_list_folder": lambda: dbx.files_list_folder(""),
        "team_common_get_info": lambda: dbx.team_common_get_info(),
        "sharing_list_folders": lambda: dbx.sharing_list_folders(),
    }
    
    results = {}
    for name, endpoint in endpoints.items():
        try:
            endpoint()
            results[name] = "SUCCESS"
        except Exception as e:
            results[name] = f"FAILED: {type(e).__name__}"
    
    for name, result in results.items():
        print(f"{name:<25} {result}")

def check_token_scopes():
    print("\n=== Checking Token Scopes ===")
    try:
        headers = {"Authorization": f"Bearer {DROPBOX_ACCESS_TOKEN}"}
        response = requests.post(
            "https://api.dropboxapi.com/2/check/user/scope",
            headers=headers,
            json={"scope": "account_info.read files.content.read files.metadata.read sharing.read team_info.read team_data.content.read team_data.metadata.read team_data.team_space"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("Token scopes:", data.get("scope", []))
        else:
            print(f"Error checking scopes: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

def try_team_root_access():
    print("\n=== Trying Different Team Space Access Methods ===")
    
    # Try to access team root through team API
    try:
        team_info = dbx.team_common_get_info()
        print(f"Team Common Info: {team_info}")
    except Exception as e:
        print(f"team_common_get_info: {e}")
    
    # Try to list team folders
    try:
        folders = dbx.sharing_list_folders()
        print(f"Shared folders: {len(folders.folders)}")
        for folder in folders.folders[:3]:
            print(f"  - {folder.name} ({folder.path_lower})")
    except Exception as e:
        print(f"sharing_list_folders: {e}")
    
    # Try different root path patterns
    test_paths = [
        "/",
        "/team",
        "/team-space",
        "/Propelland",
        "/propelland",
        "/company",
        "/shared"
    ]
    
    print("\nTesting root path variations:")
    for path in test_paths:
        try:
            result = dbx.files_list_folder(path, recursive=False)
            folder_count = sum(1 for entry in result.entries if isinstance(entry, dropbox.files.FolderMetadata))
            print(f"  ✓ {path}: {folder_count} folders")
            
            # Check if any company folders are present
            company_folders = [entry.name for entry in result.entries if isinstance(entry, dropbox.files.FolderMetadata) 
                             and (entry.name.startswith("01") or entry.name.startswith("02") or entry.name.startswith("03"))]
            if company_folders:
                print(f"    Company folders: {', '.join(company_folders)}")
                
        except Exception as e:
            print(f"  ✗ {path}: {type(e).__name__}")

check_api_availability()
check_token_scopes()
try_team_root_access()
