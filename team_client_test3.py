import os
from dotenv import load_dotenv
import dropbox
from dropbox import files

# Load environment variables
load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    raise SystemExit("DROPBOX_ACCESS_TOKEN missing in .env")

def main():
    try:
        print("=== Testing Team Client Configuration ===")
        
        # First, get your user account info
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        
        # Your team member ID (from previous test)
        your_member_id = "dbmid:AABv9TLFJrNODzmFTQPD31hy9gJX6D7nRgQ"
        
        # Create a user-specific client
        dbx = dbx_team.as_user(your_member_id)
        
        print(f"\n=== Accessing User Account ===")
        
        # List root directory
        result = dbx.files_list_folder("", recursive=False)
        print(f"Total root entries: {len(result.entries)}")
        
        folders = [entry for entry in result.entries if isinstance(entry, files.FolderMetadata)]
        files_count = len([entry for entry in result.entries if not isinstance(entry, files.FolderMetadata)])
        
        print(f"Folders: {len(folders)}, Files: {files_count}")
        
        # Check for company folders
        print("\n=== Searching for Company Folders ===")
        company_folders = []
        for entry in folders:
            if entry.name.startswith("01") or entry.name.startswith("02") or entry.name.startswith("03"):
                company_folders.append(entry)
        
        print(f"Company folders found: {len(company_folders)}")
        
        if company_folders:
            print("\n=== Company Folders ===")
            for folder in sorted(company_folders, key=lambda x: x.name):
                print(f"- {folder.name} ({folder.path_lower})")
                
                # Try to list first folder contents
                if company_folders.index(folder) == 0:
                    try:
                        sub_result = dbx.files_list_folder(folder.path_lower, recursive=False)
                        sub_folders = [e.name for e in sub_result.entries if isinstance(e, files.FolderMetadata)]
                        print(f"  Contains {len(sub_folders)} subfolders")
                        
                        if sub_folders:
                            print(f"  Subfolders: {', '.join(sub_folders[:3])}{'...' if len(sub_folders) > 3 else ''}")
                            
                    except Exception as e:
                        print(f"  Error listing contents: {e}")
                        
        else:
            print("No company folders found at root")
            print("\n=== Visible Folders ===")
            for folder in sorted(folders, key=lambda x: x.name):
                print(f"- {folder.name}")
                
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
