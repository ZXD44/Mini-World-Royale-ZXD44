import os
import shutil
import time
from pathlib import Path

# --- SMART STRUCTURE (No Emojis) ---
STRUCTURE = {
    "Documentation": {
        "files": [".md", ".pdf", ".txt"],
        "folders": ["REPORTS"]
    },
    "Testing": {
        "files": ["test_", ".spec", ".test"],
        "folders": ["tests"]
    },
    "SystemCore": {
        "folders": ["QtScrcpy_Pro", "configs"]
    },
    "Project_Utils": {
        "folders": ["scripts"]
    },
    "Trash": {
        "names": ["old", "temp", "backup", "archive", "legacy"]
    }
}

MAIN_LAUNCHERS = ["MWR_Controller.py", "Start_Game.sh"]

def smart_organize(project_dir="."):
    base = Path(project_dir).resolve()
    print(f"Starting Smart Organization: {base.name}")
    print("-" * 50)

    # 0. Recover from previous folders (including emoji versions)
    old_folders = [
        "Others", "Docs", "Tests", "Trash_ขยะ", "📦_Others", 
        "🌐_Documentation", "🧪_Testing", "⚙️_SystemCore", 
        "🛠️_Project_Utils", "🗑️_Trash", "📦_Archive_Others"
    ]
    for old_folder in old_folders:
        p = base / old_folder
        if p.exists() and p.is_dir():
            print(f"Recovering from {old_folder}...")
            for item in list(p.iterdir()):
                try:
                    target_name = item.name
                    # Avoid duplicate names on move
                    if (base / target_name).exists():
                         target_name = f"{item.stem}_{int(time.time())}{item.suffix}" if item.is_file() else f"{item.name}_{int(time.time())}"
                    
                    shutil.move(str(item), str(base / target_name))
                except:
                    pass
            # Remove old directory if empty
            try:
                p.rmdir()
            except:
                pass

    # 1. Start clean organization
    counts = {}
    for item in list(base.iterdir()):
        if item.name.startswith(".") or item.suffix == ".py":
            continue
        
        if item.name in MAIN_LAUNCHERS:
            print(f"Launch Button: {item.name} -> [ROOT]")
            continue

        target_folder = "Others"
        name_lower = item.name.lower()

        found = False
        for folder, rule in STRUCTURE.items():
            if "names" in rule and any(word in name_lower for word in rule["names"]):
                target_folder = folder
                found = True
                break
            
            if item.is_dir() and "folders" in rule and item.name in rule["folders"]:
                target_folder = folder
                found = True
                break
            
            if item.is_file() and "files" in rule:
                if any(name_lower.startswith(f) or item.suffix.lower() == f for f in rule["files"]):
                    target_folder = folder
                    found = True
                    break

        if found or item.is_file() or item.is_dir():
            try:
                (base / target_folder).mkdir(exist_ok=True)
                dest = base / target_folder / item.name
                
                if dest.exists():
                    timestamp = int(time.time())
                    dest_name = f"{item.stem}_{timestamp}{item.suffix}" if item.is_file() else f"{item.name}_{timestamp}"
                    dest = base / target_folder / dest_name
                
                shutil.move(str(item), str(dest))
                counts[target_folder] = counts.get(target_folder, 0) + 1
                print(f"Moved {item.name} -> {target_folder}")
            except Exception as e:
                print(f"Could not move {item.name}: {e}")

    print("-" * 50)
    print("Organization Complete (Clean Style):")
    for folder, count in sorted(counts.items()):
        print(f"  {folder}: {count} items")
    print("-" * 50)
    print("Main scripts are at root for convenience.")

if __name__ == "__main__":
    smart_organize()
