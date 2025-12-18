from pathlib import Path
from PIL import Image
import logging

def export_comic_to_pdf(chapter_dir, pdf_path):
    image_files = sorted(
        [p for p in chapter_dir.iterdir()
         if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    )

    if not image_files:
        logging.warning(f"No images found in {chapter_dir}, skipping PDF export.")
        return

    images = []
    for img_path in image_files:
        img = Image.open(img_path).convert("RGB")
        images.append(img)

    first, rest = images[0], images[1:]
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    first.save(
        pdf_path,
        "PDF",
        save_all=True,
        append_images=rest
    )

def scan_and_export_comics_to_pdf():
    comics_root = Path("comics")
    pdf_root = Path("comics_pdf")

    if not comics_root.exists():
        logging.warning("comics directory not found")
        return

    for author_dir in comics_root.iterdir():
        if not author_dir.is_dir():
            continue

        for comic_dir in author_dir.iterdir():
            if not comic_dir.is_dir():
                continue

            pdf_comic_dir = pdf_root / author_dir.name / comic_dir.name
            pdf_comic_dir.mkdir(parents=True, exist_ok=True)

            # 若章节目录下存在图片文件,视为合并章节,进行整本转换
            if any(p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")
                   for p in comic_dir.iterdir()):
                pdf_path = pdf_comic_dir / f"{comic_dir.name}.pdf"

                # 已转换则跳过
                if pdf_path.exists():
                    continue

                try:
                    export_comic_to_pdf(comic_dir, pdf_path)
                    print(f"[PDF] exported: {pdf_path}")
                except Exception as e:
                    logging.error(f"Failed to export PDF: {comic_dir} err={e}")

                continue

            for chapter_dir in comic_dir.iterdir():
                if not chapter_dir.is_dir():
                    continue

                pdf_path = pdf_comic_dir / f"{chapter_dir.name}.pdf"

                # 已转换则跳过
                if pdf_path.exists():
                    continue

                try:
                    export_comic_to_pdf(chapter_dir, pdf_path)
                    print(f"[PDF] exported: {pdf_path}")
                except Exception as e:
                    logging.error(f"Failed to export PDF: {chapter_dir} err={e}")
