"""
Generate index.json files for asset folders.
Usage (Windows cmd.exe):
  python generate_index.py
This will scan assets/farm and assets/prog and write index.json files listing image filenames.
"""
import os
import json

ROOT = os.path.dirname(__file__)
ASSETS = os.path.join(ROOT, 'assets')
FOLDERS = ['farm', 'prog']
EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.avif'}

for f in FOLDERS:
    folder_path = os.path.join(ASSETS, f)
    index_path = os.path.join(folder_path, 'index.json')
    if not os.path.isdir(folder_path):
        print(f"Skipping missing folder: {folder_path}")
        continue
    files = sorted([fn for fn in os.listdir(folder_path) if os.path.splitext(fn)[1].lower() in EXTS])
    if not files:
        print(f"No image files found in {folder_path}")
    else:
        with open(index_path, 'w', encoding='utf-8') as fh:
            json.dump(files, fh, indent=2)
        print(f"Wrote {index_path} ({len(files)} files)")

print('Done.')

