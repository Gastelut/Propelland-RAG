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
    print("=== Searching for team space indicators ===")
    
    # Search for possible team space folders or symlinks
    search_terms = [
        "Team Space",
        "Team Folder", 
        "Propelland",
        "Company",
        "Shared",
        "Team"
    ]
    
    all_results = {}
    for term in search_terms:
        try:
            result = dbx.files_search("", term, max_results=10)
            if result.matches:
                all_results[term] = []
                for match in result.matches:
                    entry = match.metadata
                    if isinstance(entry, files.FolderMetadata):
                        all_results[term].append((entry.name, entry.path_lower))
        except Exception as e:
            print(f"Error searching for '{term}': {e}")
    
    print("\n=== Search Results ===")
    for term, matches in all_results.items():
        if matches:
            print(f"\nResults for '{term}':")
            for name, path in matches:
                print(f"  - {name} ({path})")
                
                # List contents of these folders to see if they contain the company structure
                try:
                    contents = dbx.files_list_folder(path, recursive=False)
                    print("    Contains:")
                    for sub_entry in contents.entries:
                        if isinstance(sub_entry, files.FolderMetadata):
                            print(f"      [Folder] {sub_entry.name}")
                        else:
                            print(f"      [File] {sub_entry.name}")
                except Exception as e:
                    print(f"    Error listing contents: {e}")
                    
except Exception as e:
    print(f"Error in search: {e}")
    import traceback
    print(traceback.format_exc())
