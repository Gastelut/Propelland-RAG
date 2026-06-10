import os
from dotenv import load_dotenv
import dropbox

# Load environment variables
load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    raise SystemExit("DROPBOX_ACCESS_TOKEN missing in .env")

def main():
    try:
        print("=== Checking Team Root Information ===")
        
        # Create team client
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        
        # Get team info
        team_info = dbx_team.team_get_info()
        print("Team Info:")
        print(f"  Name: {team_info.name}")
        print(f"  ID: {team_info.id}")
        print(f"  Owner: {team_info.owner_team_member_id}")
        print()
        
        # Get current user info
        current_user = dbx_team.team_users_get_current_account()
        print("Current User:")
        print(f"  Name: {current_user.name.display_name}")
        print(f"  Email: {current_user.email}")
        print(f"  Member ID: {current_user.profile.team_member_id}")
        print()
        
        # Check root info
        print("Root Info:")
        print(f"  Root Namespace ID: {current_user.root_info.root_namespace_id}")
        print(f"  Home Namespace ID: {current_user.root_info.home_namespace_id}")
        print()
        
        # Check if user has access to team folders
        print("Checking for team folders...")
        
        # Try to get team's common folder
        try:
            common_folder = dbx_team.team_common_get_info()
            print("Team Common Folder Info:")
            print(f"  Root Namespace ID: {common_folder.root_info.root_namespace_id}")
            print(f"  Path: {common_folder.root_info.path_display}")
            
            # Try to list the common folder
            dbx = dbx_team.as_user(current_user.profile.team_member_id)
            
            try:
                # If path_display is not available, try to list from root
                # using the root namespace
                result = dbx.files_list_folder("", recursive=False)
                
                print(f"  Contents count: {len(result.entries)}")
                
                # Check if company folders are present
                company_folders = 0
                for entry in result.entries:
                    if hasattr(entry, 'name') and entry.name and (
                        entry.name.startswith("01") or 
                        entry.name.startswith("02") or 
                        entry.name.startswith("03")
                    ):
                        company_folders += 1
                        
                print(f"  Company folders detected: {company_folders}")
                
                if company_folders > 0:
                    print("  Company folders found!")
                    print("  Available folders:")
                    for entry in result.entries:
                        if hasattr(entry, 'name') and entry.name and (
                            entry.name.startswith("01") or 
                            entry.name.startswith("02") or 
                            entry.name.startswith("03")
                        ):
                            print(f"    - {entry.name}")
                            
            except Exception as e:
                print(f"  Error listing common folder: {e}")
                
        except Exception as e:
            print(f"Team Common Folder Error: {e}")
            import traceback
            print(traceback.format_exc())
            
    except Exception as e:
        print("Error:", e)
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
