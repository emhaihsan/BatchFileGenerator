# Batch File Generator → WebP/PNG/JPG/PDF

Automate personalized invitations, certificates, or letters with Python + OpenCV. This script reads one visual template plus a CSV list of recipients, then renders individualized outputs in PNG/JPG/WebP/PDF.

## Features

- **Batch processing**: one run handles dozens or hundreds of names.
- **OpenCV text rendering**: anti-aliased text looks consistent at any resolution.
- **Multi-line layout**: default template renders `[Name]`, blank line, `and family` (easy to tweak in `add_name_to_image`).
- **Multi-format output**: produce PNG, JPG, WebP, and PDF with customizable quality.

## Requirements

```bash
pip install -r requirements.txt
```

Main dependencies:
- `opencv-python` for drawing text.
- `Pillow` (used for PDF export).

## Project Structure

```
undangan/
├── README.md           # this document
├── requirements.txt    # dependencies
├── script.py           # CLI entry point
├── sample_template.png # repo-friendly PNG template
├── sample_names.csv    # public CSV sample (no personal data)
└── daftar_nama.csv     # your own working CSV (optional)
```

## Usage

1. Prepare a template image (PNG/JPG) with sufficient resolution.
2. Create a single-column CSV containing recipient names.
3. Run with the provided sample assets (multi-format):
   ```bash
   python script.py sample_template.png sample_names.csv \
       --pos 1000 900 --size 72 --color 255 255 255 \
       --formats png webp jpg pdf
   ```
4. For production, replace the sample template & CSV with your own files (pick any output formats you need).
5. Results are written to `output/` following `001_Name.ext` naming per format.

## CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `image` | Path to the invitation/certificate template | required |
| `names_csv` | CSV file containing recipient names (first column only) | required |
| `-o/--output` | Destination folder | `output` |
| `--size` | Font scale (higher value = larger strokes) | `300` |
| `--pos X Y` | Text center position in pixels (X horizontal, Y vertical) | `50 50` |
| `--color R G B` | Text color in RGB | `0 0 0` |
| `--formats FMT [FMT ...]` | Output formats (`png`, `jpg`, `webp`, `pdf`) | `webp` |

> **Note:** Stroke thickness follows the internal formula (`thickness ~ size/15`). Adjust it in `add_name_to_image` if you need a different look.

## Sample CSV

```csv
Company Name
Organization Name
Foundation Name
```

## Customization

- **Text content**: edit the `lines` list in `add_name_to_image` to control line count, spacing, or include greetings/labels. See @script.py#33-52.
- **Thickness & font**: tweak `thickness` and `font_face` to match your style. OpenCV offers `FONT_HERSHEY_SIMPLEX`, `FONT_HERSHEY_SCRIPT_SIMPLEX`, etc.
- **WebP quality**: adjust `cv2.IMWRITE_WEBP_QUALITY` inside `save_image` if you prefer different compression.

## Production Tips

- Use a high-resolution template so text stays crisp when printed.
- If names are very long, reduce `--size` or split them into multiple lines.
- Keep generated output outside the repo (or git-ignored) if it contains sensitive information.

## License

MIT License. Feel free to fork and customize.
