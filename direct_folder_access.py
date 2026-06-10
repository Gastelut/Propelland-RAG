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
        print("=== Direct Folder Access Test ===")
        
        # Create team client and access your user account
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        dbx = dbx_team.as_user(YOUR_MEMBER_ID)
        
        # Test access to a specific client project folder we found
        client_project_path = "/jorge alvarez�s files/shared/paula vega home content/folder org/01 client projects"
        
        print("Checking client projects folder...")
        
        try:
            folder_metadata = dbx.files_get_metadata(client_project_path)
            print("Successfully accessed the folder")
            print("Name:", folder_metadata.name)
            print("Path:", folder_metadata.path_lower)
            
            # List contents
            contents = dbx.files_list_folder(client_project_path, recursive=False)
            print("\nContents:")
            for entry in contents.entries:
                if isinstance(entry, files.FolderMetadata):
                    print("[FOLDER]", entry.name)
                else:
                    print("[FILE]", entry.name)
                    
        except Exception as e:
            print("Error accessing folder:", type(e).__name__, str(e))
            
    except Exception as e:
        print("Error:", e)
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
