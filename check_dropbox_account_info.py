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
    # Get account info
    account_info = dbx.users_get_current_account()
    print("=== Current Account Info ===")
    print(f"Name: {account_info.name.display_name}")
    print(f"Email: {account_info.email}")
    print(f"Account ID: {account_info.account_id}")
    print(f"Country: {account_info.country}")
    
    # Check for team info
    if hasattr(account_info, 'team'):
        print("\n=== Team Info ===")
        print(f"Team Name: {account_info.team.name}")
        print(f"Team ID: {account_info.team.id}")
    else:
        print("\n=== Not a team account ===")
        
    # Check root info
    print("\n=== Root Info ===")
    print(f"Root Namespace ID: {account_info.root_info.root_namespace_id}")
    print(f"Root Path Type: {account_info.root_info.root_path_type}")
    
    if hasattr(account_info.root_info, 'home_namespace_id'):
        print(f"Home Namespace ID: {account_info.root_info.home_namespace_id}")
        
except Exception as e:
    print(f"Error getting account info: {e}")
    import traceback
    print(traceback.format_exc())
