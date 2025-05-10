# Quick Start Guide - Deteksi Wajah dengan Haar Cascade

*Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)*

Panduan singkat ini akan membantu Anda memulai dengan aplikasi Deteksi Wajah dengan Haar Cascade dengan cepat dan mudah.

## Prasyarat

1. Python 3.6 atau yang lebih baru
2. Webcam yang berfungsi (untuk deteksi real-time)
3. Koneksi internet (untuk mengunduh file cascade jika diperlukan)

## Instalasi Cepat (Windows)

1. Pastikan Anda telah mengunduh dan mengekstrak proyek ini
2. Jalankan file `init-project.bat` untuk menginisialisasi lingkungan dan menginstal dependensi
3. Setelah selesai, Anda siap menggunakan aplikasi

## Mulai Menggunakan Aplikasi

### Opsi 1: Aplikasi Desktop (Direkomendasikan untuk Pemula)

1. Klik dua kali pada file `start-desktop-app.bat`
2. Di aplikasi desktop, klik tombol "Mulai Server Web"
3. Setelah server berjalan, klik tombol "Buka Browser"
4. Browser akan terbuka dan menampilkan antarmuka web aplikasi

### Opsi 2: Langsung ke Aplikasi Web

1. Klik dua kali pada file `start-web-app.bat`
2. Browser akan terbuka secara otomatis, atau Anda dapat mengakses `http://localhost:5000`

### Opsi 3: Menggunakan Notebook Jupyter

1. Jalankan Jupyter Notebook dari command prompt:
   ```
   jupyter notebook
   ```
2. Buka file `deteksi_lokal.ipynb` dari folder proyek
3. Jalankan sel kode dalam notebook

## Penggunaan Dasar

### Deteksi Wajah dengan Webcam

1. Di antarmuka web, klik tab "Webcam" (tab default)
2. Klik tombol "Mulai Deteksi"
3. Izinkan akses ke webcam jika diminta
4. Wajah yang terdeteksi akan ditandai dengan kotak hijau
5. Klik "Berhenti" untuk menghentikan deteksi

### Deteksi Wajah pada Gambar

1. Di antarmuka web, klik tab "Unggah Gambar"
2. Klik "Choose File" dan pilih foto yang berisi wajah
3. Klik "Deteksi Wajah"
4. Hasil deteksi akan ditampilkan dengan wajah yang ditandai kotak hijau

## Tips Performa

- Pastikan pencahayaan yang baik untuk hasil deteksi terbaik
- Posisikan wajah menghadap kamera secara langsung
- Jika deteksi tidak optimal, coba atur parameter di file `.env`

## Langkah Selanjutnya

Untuk informasi lebih lanjut:
- Lihat `web_interface.md` untuk panduan lengkap antarmuka web
- Lihat `usage.md` untuk detail lebih dalam tentang cara kerja aplikasi
- Periksa `README.md` untuk informasi umum tentang proyek

## Pemecahan Masalah Cepat

- **Webcam tidak terdeteksi**: Pastikan tidak ada aplikasi lain yang menggunakan webcam dan coba restart aplikasi
- **Deteksi tidak akurat**: Periksa pencahayaan dan posisikan wajah dengan jelas di depan kamera
- **Aplikasi error**: Pastikan semua dependensi terinstal dengan benar dengan menjalankan `pip install -r requirements.txt`
