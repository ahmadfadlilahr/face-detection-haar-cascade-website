# Changelog

Copyright (c) 2025, [Ahmad Fadlilah](https://github.com/ahmadfadlilah)

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.1] - 2025-05-10

### Added
- Update komprehensif pada `face_detection.py` dengan metode deteksi lanjutan
- Konsistensi implementasi algoritma deteksi di semua komponen aplikasi

## [0.3.0] - 2025-05-10

### Added
- Peningkatan akurasi deteksi wajah pada mode unggah gambar
- Implementasi multi-cascade classifiers (default, alt, alt2, profile)
- Deteksi wajah profil (tampak samping)
- Algoritma penggabungan hasil deteksi dan penghapusan duplikat
- Pra-pemrosesan gambar canggih (CLAHE, bilateral filtering, normalisasi)
- Deteksi multi-skala untuk hasil yang lebih akurat
- Pengenalan wajah dari kedua sisi profil

### Changed
- Optimalisasi performa dengan penggunaan deteksi terperinci pada interval tertentu

## [0.2.0] - 2025-05-10

### Added
- Web interface using Flask
- Image upload and processing feature
- Desktop application to launch the web server
- Integrated Jupyter notebook with web application
- Bootstrap-based responsive UI

## [0.1.0] - 2025-05-10

### Added
- Initial release
- Real-time face detection from webcam
- Face count display
- Histogram equalization for improved detection
- Automatic download of cascade files if not present
- Proper error handling
