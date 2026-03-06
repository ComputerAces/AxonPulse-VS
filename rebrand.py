import os

ROOT_DIR = r"f:\My Programs\AxonPulse VS"
IGNORE_DIRS = {".git", "__pycache__", "venv", "node_modules", ".gemini", "tmp"}
IGNORE_FILES = {"rebrand.py"}

# Files we want to explicitly process
ALLOW_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".yml", ".yaml", ".syp", ".bat", ".sh", ".qss"
}

TEXT_REPLACEMENTS = [
    ("Synapse VS", "AxonPulse VS"),
    ("Synapse", "AxonPulse"),
    ("synapse", "axonpulse"),
    ("SYNAPSE", "AXONPULSE"),
    ("SYNP", "AXON"),
    ("synp", "axon")
]

def clean_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    new_content = content
    for old, new in TEXT_REPLACEMENTS:
        new_content = new_content.replace(old, new)
        
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[*] Updated text in {filepath}")
        return True
    return False

def run_rename():
    print("--- Phase 1: Text Replacement ---")
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in ALLOW_EXTENSIONS or file in IGNORE_FILES:
                continue
            
            filepath = os.path.join(root, file)
            clean_file(filepath)

    print("\n--- Phase 2: File & Folder Renaming ---")
    for root, dirs, files in os.walk(ROOT_DIR, topdown=False):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file in IGNORE_FILES: continue
            
            new_name = file
            for old, new in TEXT_REPLACEMENTS:
                new_name = new_name.replace(old, new)
                
            if new_name != file:
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                print(f"[RENAME] {file} -> {new_name}")
                os.rename(old_path, new_path)

        for d in dirs:
            if d in IGNORE_DIRS: continue
            
            new_name = d
            for old, new in TEXT_REPLACEMENTS:
                new_name = new_name.replace(old, new)
                
            if new_name != d:
                old_path = os.path.join(root, d)
                new_path = os.path.join(root, new_name)
                print(f"[RENAME DIR] {d} -> {new_name}")
                os.rename(old_path, new_path)

if __name__ == "__main__":
    run_rename()
    print("\n[SUCCESS] Rebranding Complete.")
