"""
Generate thumbnails for images in a directory and write an index.json with entries
that include both thumbnail and full-size image filenames.

Usage:
  python scripts\generate_thumbnails.py --dir assets/farm --size 480 --format jpg --quality 80

Output:
  - assets/farm/thumbs/<image>_thumb.jpg (or .webp if chosen)
  - assets/farm/index.json contains an array of objects: {"name": "IMG_...jpg", "thumb": "thumbs/IMG_..._thumb.jpg"}

Requires: Pillow
"""

from pathlib import Path
import argparse
from PIL import Image
import json
import sys

SUPPORTED_IN = {'.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif'}


def make_thumb(src_path: Path, dest_path: Path, size: int, fmt: str, quality: int):
    img = Image.open(src_path)
    img.thumbnail((size, size), Image.LANCZOS)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs = {}
    if fmt.lower() in ('jpg', 'jpeg'):
        save_kwargs['quality'] = quality
        save_kwargs['optimize'] = True
        fmt_save = 'JPEG'
    elif fmt.lower() == 'webp':
        save_kwargs['quality'] = quality
        fmt_save = 'WEBP'
    else:
        fmt_save = fmt.upper()
    img = img.convert('RGB') if fmt_save in ('JPEG','WEBP') else img
    img.save(dest_path, fmt_save, **save_kwargs)


def build_index(folder: Path, size: int, fmt: str, quality: int, out_name: str = 'index.json'):
    images = []
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix.lower() in SUPPORTED_IN and p.name != out_name:
            images.append(p.name)

    entries = []
    thumbs_dir = folder / 'thumbs'
    for name in images:
        src = folder / name
        base = Path(name).stem
        thumb_name = f"{base}_thumb.{fmt}"
        thumb_path = thumbs_dir / thumb_name
        try:
            make_thumb(src, thumb_path, size, fmt, quality)
        except Exception as e:
            print(f"Warning: failed to create thumb for {src}: {e}")
            thumb_name = name  # fallback to original
        entries.append({'name': name, 'thumb': f"thumbs/{thumb_name}"})

    out_path = folder / out_name
    with out_path.open('w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    return out_path, len(entries)


def main(argv=None):
    p = argparse.ArgumentParser(description='Generate thumbnails and index.json for an images folder')
    p.add_argument('--dir', '-d', default=str(Path(__file__).resolve().parent.parent / 'assets' / 'farm'), help='Target images directory')
    p.add_argument('--size', type=int, default=480, help='Maximum thumbnail size (px)')
    p.add_argument('--format', default='jpg', choices=['jpg','webp'], help='Thumbnail file format')
    p.add_argument('--quality', type=int, default=80, help='Quality for thumbnails (1-100)')
    p.add_argument('--out', '-o', default='index.json', help='Output index filename inside the directory')
    args = p.parse_args(argv)

    folder = Path(args.dir)
    if not folder.exists() or not folder.is_dir():
        print(f"Error: directory not found: {folder}")
        return 2

    outpath, count = build_index(folder, args.size, args.format, args.quality, out_name=args.out)
    print(f"Wrote {count} entries to {outpath}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

