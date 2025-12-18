import zipfile
from pathlib import Path
import logging

def export_chapter_to_cbz(chapter_dir: Path, cbz_path: Path):
    image_files = sorted(
        [p for p in chapter_dir.iterdir()
         if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    )

    if not image_files:
        logging.warning(f"No images found in {chapter_dir}, skipping CBZ export.")
        return

    cbz_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(cbz_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for img in image_files:
            zf.write(img, arcname=img.name)

def scan_and_export_chapters_to_cbz():
    comics_root = Path("comics")
    cbz_root = Path("comics_cbz")

    if not comics_root.exists():
        logging.warning("comics directory not found")
        return

    for author_dir in comics_root.iterdir():
        if not author_dir.is_dir():
            continue

        for comic_dir in author_dir.iterdir():
            if not comic_dir.is_dir():
                continue

            cbz_comic_dir = cbz_root / author_dir.name / comic_dir.name
            cbz_comic_dir.mkdir(parents=True, exist_ok=True)

            # 若章节目录下存在图片文件,视为合并章节,进行整本转换
            if any(p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")
                   for p in comic_dir.iterdir()):
                cbz_path = cbz_comic_dir / f"{comic_dir.name}.cbz"

                # 已转换则跳过
                if cbz_path.exists():
                    continue

                try:
                    export_chapter_to_cbz(comic_dir, cbz_path)
                    print(f"[CBZ] exported: {cbz_path}")
                except Exception as e:
                    logging.error(f"Failed to export CBZ: {comic_dir} err={e}")

                continue

            for chapter_dir in comic_dir.iterdir():
                if not chapter_dir.is_dir():
                    continue

                cbz_path = cbz_comic_dir / f"{chapter_dir.name}.cbz"

                # 已转换则跳过
                if cbz_path.exists():
                    continue
                
                try:
                    export_chapter_to_cbz(chapter_dir, cbz_path)
                    print(f"[CBZ] exported: {cbz_path}")
                except Exception as e:
                    logging.error(f"Failed to export CBZ: {chapter_dir} err={e}")
