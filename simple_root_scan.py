import os
from dotenv import load_dotenv
import dropbox
from dropbox import files

# Load environment variables
load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    raise SystemExit("DROPBOX_ACCESS_TOKEN missing in .env")

# Your team member ID
YOUR_MEMBER_ID = "dbmid:AABv9TLFJrNODzmFTQPD31hy9gJX6D7nRgQ"

def main():
    try:
        print("=== Root Folder Scan ===")
        
        # Create team client and access your user account
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        dbx = dbx_team.as_user(YOUR_MEMBER_ID)
        
        # List all root contents
        root_contents = dbx.files_list_folder("", recursive=False)
        
        print(f"Total items in root: {len(root_contents.entries)}")
        print()
        
        folders = []
        
        for entry in root_contents.entries:
            if isinstance(entry, files.FolderMetadata):
                folders.append(entry)
                
        print(f"Folders in root: {len(folders)}")
        print()
        
        for i, folder in enumerate(folders, 1):
            print(f"{i}. {folder.name}")
            
        # Search for Esteban Gastelut's folder specifically
        print()
        print("=== Searching for Personal Folder ===")
        
        personal_folder = None
        
        for folder in folders:
            if "esteban" in folder.name.lower() or "gastelut" in folder.name.lower():
                personal_folder = folder
                print(f"Found personal folder: '{folder.name}'")
                print(f"Path: {folder.path_lower}")
                break
                
        if not personal_folder:
            print("Personal folder not found at root level")
            
    except Exception as e:
        print("Error:", e)
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
