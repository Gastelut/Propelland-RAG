import os
import re
import sqlite3
from pathlib import Path

DB_PATH = r"C:\Users\Bastian\propelland-rag-data\db\rag_state.sqlite"

# Search for CRM-related keywords in the Dropbox
ROOT1 = r'C:\Users\Bastian\Propelland Dropbox\01 Client Projects'
ROOT2 = r'C:\Users\Bastian\Propelland Dropbox\02 Business Development'
crm_files = []

# Search patterns for CRM-related content
patterns = [
    r'CRM',
    r'Salesforce',
    r'customer.*relationship',
    r'relationship.*management',
    r'CRM.*implementation',
    r'implement.*CRM'
]

print("=== Searching for CRM-related files in Dropbox ===")
for root_dir in [ROOT1, ROOT2]:
    if not os.path.exists(root_dir):
        print(f"Directory does not exist: {root_dir}")
        continue
        
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            
            # Check if file matches any of the CRM patterns
            if any(re.search(pattern, filename, re.IGNORECASE) for pattern in patterns):
                crm_files.append(full_path)
            
            # Check if the file is a PDF (we might want to check content later)
            if filename.lower().endswith('.pdf'):
                try:
                    # Read the first 1000 bytes of the PDF to look for CRM keywords
                    with open(full_path, 'rb') as f:
                        content = f.read(1000).decode('utf-8', errors='ignore')
                        if any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns):
                            crm_files.append(full_path)
                except Exception as e:
                    continue

if crm_files:
    print(f"\nFound {len(crm_files)} CRM-related files:")
    for filepath in sorted(crm_files):
        print(filepath)
    
    # Check if these files are in the database
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    
    print("\n=== Checking if files are indexed ===")
    for filepath in sorted(crm_files):
        cur.execute('SELECT file_id FROM files WHERE path = ?', (filepath,))
        result = cur.fetchone()
        if result:
            cur.execute('SELECT status FROM files WHERE path = ?', (filepath,))
            status = cur.fetchone()[0]
            print(f"✅ Indexed: {filepath} (Status: {status})")
        else:
            print(f"❌ Not indexed: {filepath}")
    
    con.close()
else:
    print("\nNo CRM-related files found in the current Dropbox structure")