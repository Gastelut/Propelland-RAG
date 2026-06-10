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
        print("=== Checking DropboxTeam Methods ===")
        
        # Create team client
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        
        # Get team info
        team_info = dbx_team.team_get_info()
        print("Team Info:")
        print(f"  Name: {team_info.name}")
        print()
        
        # List all available team methods
        print("Available Team Methods:")
        methods = [method for method in dir(dbx_team) if not method.startswith('_') and callable(getattr(dbx_team, method))]
        
        # Filter methods that look relevant
        relevant_methods = []
        for method in methods:
            if 'user' in method.lower() or 'team' in method.lower() or 'member' in method.lower() or 'root' in method.lower() or 'common' in method.lower():
                relevant_methods.append(method)
        
        print(f"Found {len(relevant_methods)} relevant methods:")
        for method in sorted(relevant_methods):
            print(f"  - {method}")
            
        print()
        
        # Check if 'team_common_get_info' is available
        if hasattr(dbx_team, 'team_common_get_info'):
            print("✓ team_common_get_info available")
            
            try:
                common_folder = dbx_team.team_common_get_info()
                print(f"  Root Namespace ID: {common_folder.root_info.root_namespace_id}")
                print(f"  Path: {common_folder.root_info.path_display}")
                
            except Exception as e:
                print(f"  Error: {e}")
                import traceback
                print(traceback.format_exc())
        else:
            print("✗ team_common_get_info not available")
            
        # Try to get user info through team_members_list
        if hasattr(dbx_team, 'team_members_list'):
            print("\nChecking team members...")
            members = dbx_team.team_members_list()
            print(f"Found {len(members.members)} team members")
            
            # Find your entry
            for member in members.members:
                if member.profile.email == "esteban.gastelut@propelland.com":
                    print(f"Your entry:")
                    print(f"  Name: {member.profile.name.display_name}")
                    print(f"  Email: {member.profile.email}")
                    print(f"  Member ID: {member.profile.team_member_id}")
                    
    except Exception as e:
        print("Error:", e)
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
