# Batch File Generator → WebP/PNG/JPG/PDF

Automasi penulisan nama pada undangan, sertifikat, atau surat dengan Python + OpenCV. Script ini membaca satu template gambar dan daftar nama dalam CSV, lalu menghasilkan file personalized lengkap dalam format PNG/JPG/WebP/PDF.

## Fitur

- **Batch processing**: satu perintah untuk puluhan hingga ratusan nama.
- **OpenCV text rendering**: ketebalan anti-aliasing konsisten di berbagai resolusi.
- **Multi-line layout**: template default `[Nama]`, baris kosong, `sekeluarga` (mudah diubah di fungsi `add_name_to_image`).
- **Output multi-format**: ukuran file dapat disesuaikan dalam format PNG, JPG, WebP, dan PDF.

## Prasyarat

```bash
pip install -r requirements.txt
```

Dependensi utama:
- `opencv-python` untuk menggambar teks.

## Struktur Proyek

```
undangan/
├── README.md           # dokumen ini
├── requirements.txt    # dependensi
├── script.py           # CLI utama
├── sample_template.png # template PNG bebas pakai di repo
├── sample_names.csv    # contoh CSV publik (tanpa data sensitif)
└── daftar_nama.csv     # file kerja Anda sendiri (opsional)
```

## Cara Pakai

1. Siapkan gambar undangan (PNG/JPG). Pastikan resolusi cukup tinggi.
2. Buat CSV satu kolom berisi daftar nama.
3. Jalankan dengan aset contoh (multi-format):
   ```bash
   python script.py sample_template.png sample_names.csv \
       --pos 1000 900 --size 72 --color 255 255 255 \
       --formats png webp jpg pdf
   ```
4. Untuk produksi, ganti argumen dengan template & CSV milik Anda (format bisa dipilih sesuka hati).
5. Keluaran berada di folder `output/` dengan pola `001_Nama.ext` sesuai format.

## Argumen CLI

| Argumen | Deskripsi | Default |
|---------|-----------|---------|
| `image` | Path gambar template undangan | wajib |
| `names_csv` | Path CSV daftar nama (kolom pertama dibaca) | wajib |
| `-o/--output` | Folder tujuan keluaran | `output` |
| `--size` | Skala font (proporsional, semakin besar semakin tebal) | `300` |
| `--pos X Y` | Titik tengah teks dalam piksel (X horizontal, Y vertikal) | `50 50` |
| `--color R G B` | Warna teks RGB | `0 0 0` |
| `--formats FMT [FMT ...]` | Daftar format output (`png`, `jpg`, `webp`, `pdf`) | `webp` |

> **Catatan:** Ketebalan huruf mengikuti rumus internal (`thickness ~ size/15`). Untuk personalisasi, ubah rumus pada fungsi `add_name_to_image` di `script.py`.

## Format CSV Contoh

```csv
PT. Sejahtera Bersama
CV. Maju Jaya
Yayasan Pendidikan Nusantara
```

## Kustomisasi

- **Konten teks**: ubah daftar `lines` di fungsi `add_name_to_image` untuk menentukan berapa baris, spacing, atau placeholder lain (mis. tambahkan salam atau keterangan). Lihat @script.py#33-52.
- **Ketebalan & font**: ubah variabel `thickness` dan `font_face` agar sesuai gaya yang diinginkan. OpenCV menyediakan beberapa pilihan (`FONT_HERSHEY_SIMPLEX`, `FONT_HERSHEY_SCRIPT_SIMPLEX`, dll.).
- **Kualitas WebP**: parameter `cv2.IMWRITE_WEBP_QUALITY` di akhir fungsi dapat diganti jika ingin kualitas/ukuran berbeda.

## Tips Produksi

- Gunakan template resolusi tinggi supaya teks tidak pecah saat dicetak.
- Jika teks terlalu panjang melewati margin, pertimbangkan mengecilkan `--size` atau membagi nama jadi dua baris.
- Simpan output dalam repositori terpisah atau git-ignored folder bila memproses data sensitif.

## Lisensi

MIT License. Silakan fork dan kembangkan sesuai kebutuhan.
