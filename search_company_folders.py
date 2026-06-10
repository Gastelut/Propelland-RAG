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
        print("=== Searching for Company Folders ===")
        
        # Create team client and access your user account
        dbx_team = dropbox.DropboxTeam(DROPBOX_ACCESS_TOKEN)
        dbx = dbx_team.as_user(YOUR_MEMBER_ID)
        
        # Company folder patterns to search for
        company_folder_patterns = [
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
            "11 Admin",
            "12 Propelland Brand",
            "13 Finance",
            "14 Propelland 10 years"
        ]
        
        all_matches = {}
        
        print("Searching for company folders...")
        
        for pattern in company_folder_patterns:
            try:
                results = dbx.files_search("", pattern, max_results=10)
                if results.matches:
                    matches = []
                    for match in results.matches:
                        if isinstance(match.metadata, files.FolderMetadata):
                            matches.append((match.metadata.name, match.metadata.path_lower))
                    if matches:
                        all_matches[pattern] = matches
                        
            except Exception as e:
                print(f"Error searching for '{pattern}': {e}")
        
        print(f"\nFound matches for {len(all_matches)} folder patterns")
        
        for pattern, matches in all_matches.items():
            print(f"\n=== {pattern} ===")
            for name, path in matches:
                print(f"- {name}")
                print(f"  Path: {path}")
                
                try:
                    # List first few contents
                    contents = dbx.files_list_folder(path, recursive=False)
                    subfolders = []
                    files_count = 0
                    
                    for entry in contents.entries:
                        if isinstance(entry, files.FolderMetadata):
                            subfolders.append(entry.name)
                        else:
                            files_count += 1
                    
                    if subfolders or files_count > 0:
                        print(f"  Contents: {len(subfolders)} folders, {files_count} files")
                        
                        if subfolders:
                            print(f"  Subfolders: {', '.join(subfolders[:3])}{'...' if len(subfolders) > 3 else ''}")
                            
                except Exception as e:
                    print(f"  Error listing contents: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
