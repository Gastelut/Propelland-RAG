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
    # Get account info
    account_info = dbx.users_get_current_account()
    print("=== Account Info ===")
    print(f"Name: {account_info.name.display_name}")
    print(f"Team: {account_info.team.name}")
    
    # Try different approaches to find the team space
    print("\n=== Trying to access team space ===")
    
    # Approach 1: Check if there's a "Team Space" or "Company" folder
    search_result = dbx.files_search("", "team", max_results=5)
    if search_result.matches:
        print("\nSearch results for 'team':")
        for match in search_result.matches:
            entry = match.metadata
            print(f"  {entry.name} ({entry.path_lower})")
    
    search_result = dbx.files_search("", "company", max_results=5)
    if search_result.matches:
        print("\nSearch results for 'company':")
        for match in search_result.matches:
            entry = match.metadata
            print(f"  {entry.name} ({entry.path_lower})")
    
    # Approach 2: Check if we're in team space or user space
    print("\n=== Current root path ===")
    print(f"Root namespace: {account_info.root_info.root_namespace_id}")
    
    # Try to list root with include_media_info to see if there's any difference
    result = dbx.files_list_folder("", recursive=False, include_media_info=True)
    print(f"\nRoot folder has {len(result.entries)} entries")
    
    # Approach 3: Try to use team namespace
    if hasattr(account_info, 'team'):
        print(f"\n=== Team Info ===")
        print(f"Team ID: {account_info.team.id}")
        
        # Try to list team folders via team API
        try:
            # This might require different permissions
            team_result = dbx.team_common_get_info()
            print(f"Team Common Folder: {team_result.root_info.root_namespace_id}")
            
            team_root = dbx.files_list_folder("", recursive=False, include_deleted=False)
            print(f"Team root has {len(team_root.entries)} entries")
            
        except Exception as e:
            print(f"Error accessing team info: {e}")
            import traceback
            print(traceback.format_exc())
            
except Exception as e:
    print(f"Error accessing team space: {e}")
    import traceback
    print(traceback.format_exc())
