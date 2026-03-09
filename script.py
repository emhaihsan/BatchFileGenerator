#!/usr/bin/env python3
"""
Batch File Generator: personalisasi gambar (template + CSV) menjadi berbagai format.
"""

import argparse
import csv
from pathlib import Path

import cv2
from PIL import Image

def load_names(csv_path):
    """Baca nama dari CSV (kolom pertama)."""
    names = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                names.append(row[0].strip())
    return names

SUPPORTED_FORMATS = {"png", "jpg", "jpeg", "webp", "pdf"}


def render_personalized_image(image_path, name, font_size=300,
                              position=(50, 50), color=(0, 0, 0)):
    """Kembalikan array gambar (BGR) yang sudah ditambahkan teks."""
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Gagal membuka gambar: {image_path}")

    font_face = cv2.FONT_HERSHEY_DUPLEX
    font_scale = max(font_size / 30.0, 0.1)
    thickness = max(int(font_scale * 2), 1)
    line_spacing = int(font_size * 0.25)
    bgr_color = tuple(int(c) for c in reversed(color))

    lines = [
        f"{name}",
        " ",
        "sekeluarga",
    ]

    y_offset = position[1]
    for line in lines:
        text_size, baseline = cv2.getTextSize(line, font_face, font_scale, thickness)
        line_width, line_height = text_size
        x = int(position[0] - line_width / 2)
        y = int(y_offset + line_height)
        cv2.putText(
            img,
            line,
            (x, y),
            font_face,
            font_scale,
            bgr_color,
            thickness,
            lineType=cv2.LINE_AA
        )
        y_offset += line_height + line_spacing

    return img


def save_image(img, output_path, fmt):
    fmt = fmt.lower()
    if fmt == "pdf":
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        pil_img.save(output_path, "PDF")
        return True

    params = []
    if fmt == "webp":
        params = [cv2.IMWRITE_WEBP_QUALITY, 85]
    elif fmt in ("jpg", "jpeg"):
        params = [cv2.IMWRITE_JPEG_QUALITY, 90]
    success = cv2.imwrite(str(output_path), img, params)
    return success

def main():
    parser = argparse.ArgumentParser(description="Batch File Generator: template + CSV → multi-format output")
    parser.add_argument('image', help='Path gambar undangan (PNG/JPG/etc.)')
    parser.add_argument('names_csv', help='CSV berisi daftar nama')
    parser.add_argument('-o', '--output', default='output', help='Folder output (default: output)')
    parser.add_argument('--size', type=int, default=300, help='Skala font OpenCV (pixel)')
    parser.add_argument('--pos', nargs=2, type=int, default=[50, 50], metavar=('X', 'Y'),
                        help='Posisi teks (default: 50 50)')
    parser.add_argument('--color', nargs=3, type=int, default=[0, 0, 0], metavar=('R', 'G', 'B'),
                        help='Warna RGB (default: 0 0 0)')
    parser.add_argument('--formats', nargs='+', default=['webp'], metavar='FMT',
                        help='Format keluaran (pilihan: png jpg webp pdf). Bisa lebih dari satu.')

    args = parser.parse_args()

    invalid = [fmt for fmt in args.formats if fmt.lower() not in SUPPORTED_FORMATS]
    if invalid:
        raise ValueError(f"Format tidak didukung: {', '.join(invalid)}")

    names = load_names(args.names_csv)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, name in enumerate(names, 1):
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        base_name = out_dir / f"{i:03d}_{safe_name}"
        personalized = render_personalized_image(
            args.image,
            name,
            font_size=args.size,
            position=tuple(args.pos),
            color=tuple(args.color)
        )
        for fmt in args.formats:
            fmt_lower = fmt.lower()
            ext = 'jpg' if fmt_lower == 'jpeg' else fmt_lower
            out_path = base_name.with_suffix(f'.{ext}')
            if save_image(personalized, str(out_path), fmt_lower):
                print(f"✅ {out_path}")
            else:
                raise RuntimeError(f"Gagal menyimpan {fmt_lower.upper()} untuk {name}")

if __name__ == '__main__':
    main()