@echo off
echo Menginisialisasi lingkungan untuk aplikasi Deteksi Wajah...
echo Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
echo.

REM Membuat direktori notebooks jika belum ada
if not exist notebooks mkdir notebooks

REM Membuat direktori dist jika belum ada (untuk distribusi)
if not exist dist mkdir dist

REM Copy notebook ke direktori notebooks jika belum ada
if exist deteksi_lokal.ipynb (
    if not exist notebooks\deteksi_lokal.ipynb copy deteksi_lokal.ipynb notebooks\deteksi_lokal.ipynb
)

REM Membuat file .env dari .env.example jika belum ada
if not exist .env (
    if exist .env.example copy .env.example .env
    echo File .env dibuat dari template.
)

REM Menginstal dependensi
echo Menginstal dependensi...
pip install -r requirements.txt

echo.
echo Inisialisasi selesai! Anda dapat menjalankan aplikasi dengan:
echo - start-desktop-app.bat untuk aplikasi desktop
echo - start-web-app.bat untuk aplikasi web
echo.

pause
