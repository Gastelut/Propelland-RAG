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
        print("=== Finding Esteban Gastelut's Personal Folder ===")
        
        # Create team client and access your user account
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        dbx = dbx_team.as_user(YOUR_MEMBER_ID)
        
        # Search for folders containing your name
        print("Searching for folders containing 'Esteban' or 'Gastelut'...")
        
        # Search for your personal folder
        results = dbx.files_search("", "Esteban Gastelut", max_results=10)
        
        if results.matches:
            print(f"Found {len(results.matches)} folders containing your name:")
            
            for i, match in enumerate(results.matches):
                if isinstance(match.metadata, files.FolderMetadata):
                    print(f"\n{i+1}. Name: {match.metadata.name}")
                    print(f"   Path: {match.metadata.path_lower}")
                    
                    try:
                        # List contents of this folder
                        contents = dbx.files_list_folder(match.metadata.path_lower, recursive=False)
                        
                        folders = [entry for entry in contents.entries if isinstance(entry, files.FolderMetadata)]
                        files_count = len([entry for entry in contents.entries if not isinstance(entry, files.FolderMetadata)])
                        
                        print(f"   Contents: {len(folders)} folders, {files_count} files")
                        
                        if folders:
                            print(f"   Folders:")
                            for subfolder in folders:
                                print(f"     - {subfolder.name}")
                                
                    except Exception as e:
                        print(f"   Error listing contents: {e}")
                        
        else:
            print("No folders containing your name found")
            
        # Also search for your personal folder in root
        print("\n=== Root Folder Contents ===")
        root_contents = dbx.files_list_folder("", recursive=False)
        
        print(f"Total items in root: {len(root_contents.entries)}")
        
        for entry in root_contents.entries:
            if isinstance(entry, files.FolderMetadata):
                if "esteban" in entry.name.lower() or "gastelut" in entry.name.lower():
                    print(f"\nYour Personal Folder:")
                    print(f"Name: {entry.name}")
                    print(f"Path: {entry.path_lower}")
                    
                    # List contents
                    try:
                        contents = dbx.files_list_folder(entry.path_lower, recursive=False)
                        
                        folders = [e for e in contents.entries if isinstance(e, files.FolderMetadata)]
                        files_count = len([e for e in contents.entries if not isinstance(e, files.FolderMetadata)])
                        
                        print(f"Contents: {len(folders)} folders, {files_count} files")
                        
                        if folders:
                            for subfolder in folders:
                                print(f"  - {subfolder.name}")
                                
                    except Exception as e:
                        print(f"Error listing contents: {e}")
                        
    except Exception as e:
        print("Error:", e)
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
