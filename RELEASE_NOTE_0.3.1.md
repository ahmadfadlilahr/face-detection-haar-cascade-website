# Release Notes - Versi 0.3.1

## Tanggal: 10 Mei 2025

## Ringkasan
Versi 0.3.1 adalah update komprehensif yang fokus pada konsistensi algoritma deteksi wajah di seluruh komponen aplikasi. Update ini memastikan bahwa file `face_detection.py` menggunakan metode deteksi lanjutan yang sama seperti yang telah diterapkan di aplikasi web.

## Perubahan Utama

### Peningkatan Akurasi Deteksi Wajah
1. **Multiple Cascade Classifiers di face_detection.py**
   - Integrasi 4 classifier: default, alt, alt2, dan profile
   - Deteksi profil untuk mengenali wajah dari tampak samping
   - Flipped image analysis untuk deteksi profil dari sisi berbeda

2. **Algoritma Penggabungan dan Penghilangan Duplikat**
   - Implementasi Non-Maximum Suppression (NMS)
   - Penghitungan Intersection over Union (IoU)
   - Pengurutan berdasarkan area wajah untuk hasil optimal

3. **Teknik Pra-pemrosesan Gambar Lanjutan**
   - CLAHE (Contrast Limited Adaptive Histogram Equalization)
   - Filter bilateral untuk mengurangi noise sambil mempertahankan tepi
   - Multi-scale detection dengan parameter berbeda

### Dokumentasi
- Update CHANGELOG.md ke versi 0.3.1
- Peningkatan versi di setup.py

### Pengujian
- Update test_webapp.py untuk menguji fitur deteksi wajah lanjutan
- Penambahan pengujian untuk fungsi merge_faces

## File yang Diperbarui
- src/face_detection.py
- CHANGELOG.md
- setup.py
- tests/test_webapp.py

## File yang Ditambahkan
- notebooks/__init__.py
- setup_deps.py
- install-dependencies.bat
