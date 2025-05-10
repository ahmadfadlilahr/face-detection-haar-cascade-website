---
layout: default
title: Deteksi Wajah dengan Haar Cascade
---

# Deteksi Wajah dengan Haar Cascade

Aplikasi deteksi wajah real-time menggunakan klasifikasi Haar Cascade dari OpenCV, dengan antarmuka desktop dan web.

Copyright (c) 2025, [Ahmad Fadlilah](https://github.com/ahmadfadlilah)

## Ikhtisar

Proyek ini mengimplementasikan sistem deteksi wajah real-time menggunakan webcam dan klasifikasi Haar Cascade dari OpenCV. Aplikasi ini mendeteksi wajah dalam video feed, menggambar persegi di sekitarnya, dan menampilkan jumlah wajah yang terdeteksi. Ekualisasi histogram diterapkan untuk meningkatkan deteksi wajah dalam kondisi pencahayaan yang bervariasi.

Proyek ini sekarang dilengkapi dengan antarmuka web untuk pengalaman yang lebih user-friendly!

## Fitur

- Deteksi wajah real-time dari webcam
- Antarmuka web untuk mengakses aplikasi melalui browser
- Unggah dan proses gambar melalui antarmuka web
- Deteksi wajah pada gambar yang diunggah
- Unduhan otomatis file cascade jika belum ada
- Tampilan jumlah wajah terdeteksi
- Ekualisasi histogram untuk deteksi yang lebih baik dalam kondisi pencahayaan bervariasi
- Penanganan error yang baik dan inisialisasi webcam yang lancar

## Demo

Lihat [notebook demo](notebooks/github_pages_demo.html) untuk demonstrasi dan penjelasan lebih lanjut tentang bagaimana cara kerja deteksi wajah.

## Dokumentasi

- [Panduan Penggunaan](docs/usage.html)
- [Panduan Cepat](docs/quickstart.html)
- [Antarmuka Web](docs/web_interface.html)

## Memulai

Untuk memulai dengan aplikasi ini, klon repositori ini dan ikuti instruksi dalam [Panduan Cepat](docs/quickstart.html).

```bash
git clone https://github.com/ahmadfadlilahr/face-detection-haar-cascade.git
cd face-detection-haar-cascade
pip install -r requirements.txt
```

## Persyaratan

- Python 3.6 atau lebih baru
- OpenCV
- NumPy
- Requests
- Flask (untuk antarmuka web)

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detail.
