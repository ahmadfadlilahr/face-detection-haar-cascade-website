# Deteksi Wajah dengan Haar Cascade

Aplikasi deteksi wajah real-time menggunakan klasifikasi Haar Cascade dari OpenCV, dengan antarmuka desktop dan web.

Copyright (c) 2025, [Ahmad Fadlilah](https://github.com/ahmadfadlilah)

## Gambaran Umum

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

## Persyaratan

- Python 3.x
- OpenCV
- NumPy
- Requests
- Flask (untuk antarmuka web)

## Instalasi

1. Clone repositori ini:
```
git clone https://github.com/username-anda/face-detection-haar-cascade.git
cd face-detection-haar-cascade
```

2. Jalankan file init-project.bat untuk inisialisasi awal, atau instal dependensi secara manual:
```
init-project.bat
```

Atau:
```
pip install -r requirements.txt
```

## Penggunaan

### Antarmuka Web

Untuk menjalankan aplikasi dengan antarmuka web:

```
python src/app.py
```

Atau cukup jalankan file batch yang disediakan:
```
start-web-app.bat
```

Kemudian buka browser dan navigasikan ke:
```
http://localhost:5000
```

### Aplikasi Desktop

Untuk menjalankan aplikasi desktop launcher:

```
python src/desktop_app.py
```

Atau cukup jalankan file batch yang disediakan:
```
start-desktop-app.bat
```

### Command Line

Untuk menjalankan aplikasi deteksi wajah asli dari command line:

```
python src/face_detection.py
```

### Jupyter Notebook

Atau buka dan jalankan Jupyter notebook:

```
jupyter notebook deteksi_lokal.ipynb
```

Tekan 'q' untuk keluar dari aplikasi command-line saat sedang berjalan.

## Struktur Proyek

```
├── LICENSE
├── README.md
├── README_ID.md
├── requirements.txt
├── src/
│   ├── app.py               # Aplikasi web
│   ├── desktop_app.py       # Desktop launcher untuk app web
│   ├── face_detection.py    # Modul inti deteksi wajah
│   └── templates/           # Template web
│       └── index.html       # Antarmuka web utama
└── deteksi_lokal.ipynb      # Implementasi notebook Jupyter
```

## Pemecahan Masalah

### Webcam tidak terdeteksi

Pastikan:
1. Webcam terhubung dengan benar ke komputer
2. Tidak ada aplikasi lain yang menggunakan webcam pada saat yang sama
3. Anda telah memberikan izin browser untuk mengakses webcam

### Deteksi wajah kurang akurat

Coba:
1. Pastikan pencahayaan cukup baik
2. Posisikan wajah tepat di depan kamera
3. Ubah parameter `scaleFactor` dan `minNeighbors` di kode sumber untuk penyesuaian

### Aplikasi web tidak berjalan

Periksa:
1. Pastikan semua dependensi telah terinstal dengan benar (`pip install -r requirements.txt`)
2. Pastikan port 5000 tidak digunakan oleh aplikasi lain
3. Periksa pesan error di terminal tempat Anda menjalankan aplikasi
