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
        print("=== Checking Team Folders ===")
        
        # Create team client
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        
        # Check if team folder methods are available
        if hasattr(dbx_team, 'team_team_folder_list'):
            print("team_team_folder_list available")
            
            # List all team folders
            team_folders = dbx_team.team_team_folder_list()
            print(f"Found {len(team_folders.team_folders)} team folders")
            
            if team_folders.team_folders:
                print()
                for folder in team_folders.team_folders:
                    print(f"Folder Name: {folder.name}")
                    print(f"  ID: {folder.team_folder_id}")
                    print(f"  Path: {folder.path_display}")
                    print(f"  Namespace ID: {folder.root_info.root_namespace_id}")
                    print()
                    
                    # Try to access this folder
                    try:
                        # Create user client using your member ID
                        YOUR_MEMBER_ID = "dbmid:AABv9TLFJrNODzmFTQPD31hy9gJX6D7nRgQ"
                        dbx = dbx_team.as_user(YOUR_MEMBER_ID)
                        
                        # Try to list folder contents
                        result = dbx.files_list_folder(folder.path_display, recursive=False)
                        print(f"  Contents: {len(result.entries)} items")
                        
                        for entry in result.entries[:5]:
                            if hasattr(entry, 'name'):
                                print(f"    - {entry.name}")
                        
                        if len(result.entries) > 5:
                            print(f"    ... and {len(result.entries) - 5} more")
                            
                    except Exception as e:
                        print(f"  Error listing contents: {e}")
                        
            else:
                print("No team folders found")
        else:
            print("team_team_folder_list not available")
            
    except Exception as e:
        print("Error:", e)
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
