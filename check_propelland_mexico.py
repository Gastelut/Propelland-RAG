import os
from dotenv import load_dotenv
import dropbox
from dropbox import files

# Load environment variables
load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    raise SystemExit("DROPBOX_ACCESS_TOKEN missing in .env")

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

try:
    print("=== Checking Propelland Mexico Migration ===")
    
    # List contents of Propelland Mexico Migration
    folder_path = "/Propelland Mexico Migration"
    result = dbx.files_list_folder(folder_path, recursive=False)
    
    print(f"Contains {len(result.entries)} items")
    
    print("\n=== Folder Contents ===")
    print(f"Path: {folder_path}")
    
    # Search for folders that might contain company structure
    company_candidates = []
    
    for entry in result.entries:
        if isinstance(entry, files.FolderMetadata):
            print(f"  [Folder] {entry.name}")
            
            # Check if this folder might contain client projects or business dev
            if "propelland" in entry.name.lower() or "shared" in entry.name.lower() or "ops" in entry.name.lower():
                try:
                    subcontents = dbx.files_list_folder(entry.path_lower, recursive=False)
                    print(f"    Contains {len(subcontents.entries)} items")
                    sub_folders = [e.name for e in subcontents.entries if isinstance(e, files.FolderMetadata)]
                    
                    if any(name.startswith("01") or name.startswith("02") or name.startswith("03") for name in sub_folders):
                        print(f"    ✓ Contains numbered company folders!")
                        company_candidates.append(entry)
                        
                except Exception as e:
                    print(f"    Error listing contents: {e}")
                    
    print(f"\nFound {len(company_candidates)} possible company folder containers")
    for candidate in company_candidates:
        print(f"\n=== {candidate.name} ===")
        subcontents = dbx.files_list_folder(candidate.path_lower, recursive=False)
        for sub_entry in subcontents.entries:
            if isinstance(sub_entry, files.FolderMetadata):
                print(f"  [Folder] {sub_entry.name}")
                
except Exception as e:
    print(f"Error checking Propelland Mexico Migration: {e}")
    import traceback
    print(traceback.format_exc())
