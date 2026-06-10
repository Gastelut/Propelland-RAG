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
        print("=== List Team Folders ===")
        
        # Create team client
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        
        # List all team folders
        team_folders = dbx_team.team_team_folder_list()
        print(f"Found {len(team_folders.team_folders)} team folders")
        
        print()
        print("=== Available Team Folders ===")
        
        # Filter for company-related folders
        company_folders = []
        
        for folder in team_folders.team_folders:
            folder_name = folder.name
            print(f"- {folder_name}")
            
            # Check if it's likely a company folder
            if folder_name and (
                folder_name.startswith("01") or 
                folder_name.startswith("02") or 
                folder_name.startswith("03") or
                "Client" in folder_name or
                "Business" in folder_name or
                "Propelland" in folder_name
            ):
                company_folders.append(folder)
        
        print()
        
        if company_folders:
            print(f"=== Found {len(company_folders)} Company Folders ===")
            
            for folder in company_folders:
                print(f"Name: {folder.name}")
                print(f"ID: {folder.team_folder_id}")
                
                if hasattr(folder, 'root_info'):
                    print(f"Root Namespace ID: {folder.root_info.root_namespace_id}")
                
                print()
                
                # Try to access this folder
                try:
                    YOUR_MEMBER_ID = "dbmid:AABv9TLFJrNODzmFTQPD31hy9gJX6D7nRgQ"
                    dbx = dbx_team.as_user(YOUR_MEMBER_ID)
                    
                    # Try to get folder metadata
                    metadata = dbx.files_get_metadata(f"/{folder.name}")
                    print(f"Successfully accessed folder")
                    
                except Exception as e:
                    print(f"Error accessing folder: {e}")
                    
                print()
                
        else:
            print("No company folders found in team folder list")
            
    except Exception as e:
        print("Error:", e)
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
