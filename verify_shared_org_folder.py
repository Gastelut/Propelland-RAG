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
        
        # The path to the shared org folder
        org_folder_path = "/jorge alvarez�s files/shared/paula vega home content/folder org"
        
        print(f"Checking folder: {org_folder_path}")
        
        # Check if the folder exists and we can access it
        try:
            folder_metadata = dbx.files_get_metadata(org_folder_path)
            print("Successfully accessed the folder")
            print(f"Type: {type(folder_metadata)}")
            print(f"Name: {folder_metadata.name}")
            print(f"Path: {folder_metadata.path_lower}")
        except Exception as e:
            print(f"Error accessing folder: {e}")
            return
            
        # List all contents of this folder
        print("\n=== Folder Contents ===")
        contents = dbx.files_list_folder(org_folder_path, recursive=False)
        
        folder_count = 0
        file_count = 0
        
        for entry in contents.entries:
            if isinstance(entry, files.FolderMetadata):
                print(f"[FOLDER] {entry.name}")
                folder_count += 1
            else:
                print(f"[FILE] {entry.name}")
                file_count += 1
                
        print(f"\nTotal: {folder_count} folders, {file_count} files")
        
        # Check if this contains all the expected company folders
        expected_folders = [
            "01 Client Projects",
            "02 Business Development", 
            "03 Propelland Brand",
            "04 Competitive Intelligence & Marketing",
            "05 Team",
            "06 Tools & Frameworks",
            "07 Events & Talks",
            "08 Propel U",
            "09 Propel Org",
            "10 Propel Labs",
            "11 Admin"
        ]
        
        found_folders = [entry.name for entry in contents.entries if isinstance(entry, files.FolderMetadata)]
        
        print("\n=== Expected vs Found Folders ===")
        for folder in expected_folders:
            if folder in found_folders:
                print(f"✓ {folder}")
            else:
                print(f"✗ {folder}")
                
        # Let's check one folder's contents to see if they're valid
        test_folder = "01 Client Projects"
        if test_folder in found_folders:
            test_path = f"{org_folder_path}/{test_folder}"
            print(f"\n=== Checking '{test_folder}' ===")
            test_contents = dbx.files_list_folder(test_path, recursive=False)
            
            subfolder_count = 0
            for entry in test_contents.entries:
                if isinstance(entry, files.FolderMetadata):
                    print(f"  [FOLDER] {entry.name}")
                    subfolder_count += 1
            
            print(f"\n  Contains {subfolder_count} subfolders")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
