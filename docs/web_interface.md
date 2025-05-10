# Panduan Penggunaan Antarmuka Web

*Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)*

## Pengantar

Antarmuka web untuk aplikasi Deteksi Wajah dengan Haar Cascade menyediakan cara yang lebih mudah dan user-friendly untuk menggunakan fitur deteksi wajah. Antarmuka ini memungkinkan pengguna untuk:

1. Mendeteksi wajah secara real-time melalui webcam
2. Mengunggah gambar dan mendeteksi wajah pada gambar tersebut
3. Melihat informasi tentang aplikasi

## Menjalankan Aplikasi Web

### Metode 1: Melalui File Batch (Windows)

Cara termudah untuk menjalankan aplikasi web adalah dengan menggunakan file batch yang telah disediakan:

1. Buka folder aplikasi
2. Klik dua kali pada file `start-web-app.bat`

### Metode 2: Melalui Command Line

1. Buka terminal atau command prompt
2. Navigasikan ke folder aplikasi:
   ```
   cd "path\to\Deteksi Wajah dengan Harr Cascade"
   ```
3. Jalankan aplikasi web:
   ```
   python src/app.py
   ```

### Metode 3: Melalui Aplikasi Desktop

1. Klik dua kali pada file `start-desktop-app.bat`, atau
2. Jalankan `python src/desktop_app.py` di terminal

### Metode 4: Melalui Jupyter Notebook

1. Buka Jupyter Notebook:
   ```
   jupyter notebook
   ```
2. Buka file `deteksi_lokal.ipynb`
3. Jalankan semua sel dalam notebook

## Menggunakan Antarmuka Web

Setelah aplikasi berjalan, buka browser web Anda dan akses:
```
http://localhost:5000
```

### Tab Webcam

1. Klik tombol "Mulai Deteksi" untuk memulai deteksi wajah melalui webcam
2. Wajah yang terdeteksi akan ditandai dengan kotak hijau
3. Jumlah wajah yang terdeteksi akan ditampilkan di sudut kiri atas
4. Klik "Berhenti" untuk menghentikan deteksi

### Tab Unggah Gambar

1. Klik "Choose File" untuk memilih gambar dari komputer Anda
2. Klik tombol "Deteksi Wajah" untuk memproses gambar
3. Hasil deteksi akan ditampilkan dengan kotak hijau mengelilingi wajah terdeteksi

### Tab Tentang

Tab ini berisi informasi tentang aplikasi, teknologi yang digunakan, dan fitur-fitur yang tersedia.

## Troubleshooting

### Webcam tidak terdeteksi

Pastikan:
1. Webcam terhubung dengan benar ke komputer
2. Tidak ada aplikasi lain yang menggunakan webcam pada saat yang sama
3. Anda telah memberikan izin browser untuk mengakses webcam

### Deteksi wajah kurang akurat

Coba:
1. Pastikan pencahayaan cukup baik
2. Posisikan wajah tepat di depan kamera
3. Hindari latar belakang yang kompleks atau pencahayaan yang terlalu terang/gelap

### Aplikasi web tidak berjalan

Periksa:
1. Pastikan semua dependensi telah terinstal dengan benar (`pip install -r requirements.txt`)
2. Pastikan port 5000 tidak digunakan oleh aplikasi lain
3. Periksa pesan error di terminal tempat Anda menjalankan aplikasi
