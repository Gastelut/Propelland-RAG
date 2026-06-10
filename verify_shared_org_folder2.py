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
        print("=== Verifying Shared Org Folder Access ===")
        
        # Create team client and access your user account
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        dbx = dbx_team.as_user(YOUR_MEMBER_ID)
        
        # The path to the shared org folder (using ASCII characters only)
        org_folder_path = "/jorge alvarez?s files/shared/paula vega home content/folder org"
        
        print("Checking shared org folder...")
        
        # Check if the folder exists and we can access it
        try:
            folder_metadata = dbx.files_get_metadata(org_folder_path)
            print("Successfully accessed the folder")
            print("Name:", folder_metadata.name)
            print("Path:", folder_metadata.path_lower)
        except Exception as e:
            print("Error accessing folder:", e)
            return
            
        # List all contents of this folder
        print("\n=== Folder Contents ===")
        contents = dbx.files_list_folder(org_folder_path, recursive=False)
        
        folder_count = 0
        file_count = 0
        
        for entry in contents.entries:
            if isinstance(entry, files.FolderMetadata):
                print("[FOLDER]", entry.name)
                folder_count += 1
            else:
                print("[FILE]", entry.name)
                file_count += 1
                
        print("\nTotal:", folder_count, "folders,", file_count, "files")
        
    except Exception as e:
        print("Error:", e)
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
