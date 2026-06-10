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
    print("=== Checking API capabilities ===")
    
    # Try to get current account info with detailed scope info
    account_info = dbx.users_get_current_account()
    
    print(f"Account: {account_info.name.display_name}")
    print(f"Team: {account_info.team.name}")
    print(f"Account Type: {account_info.account_type}")
    
    # Check what endpoints we can access by trying simple operations
    print("\n=== API Endpoint Availability ===")
    
    # Try files endpoints
    try:
        dbx.files_list_folder("")
        print("OK: files_list_folder available")
    except Exception as e:
        print(f"ERROR: files_list_folder: {e}")
    
    try:
        dbx.sharing_list_folders()
        print("OK: sharing_list_folders available")
    except Exception as e:
        print(f"ERROR: sharing_list_folders: {e}")
        
    try:
        dbx.team_list_members()
        print("OK: team_list_members available")
    except Exception as e:
        print(f"ERROR: team_list_members: {e}")
        
    try:
        dbx.users_get_account(account_info.account_id)
        print("OK: users_get_account available")
    except Exception as e:
        print(f"ERROR: users_get_account: {e}")
        
except Exception as e:
    print(f"Error checking permissions: {e}")
    import traceback
    print(traceback.format_exc())
