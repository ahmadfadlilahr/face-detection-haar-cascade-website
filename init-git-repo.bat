@echo off
echo Persiapan Repositori Git untuk GitHub Pages
echo ==========================================
echo Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
echo.
echo Script ini akan membantu Anda menginisialisasi repositori Git
echo dan mempersiapkan proyek untuk deployment GitHub Pages.
echo.

REM Meminta username GitHub
set /p github_username="Masukkan username GitHub Anda: "

REM Memperbarui file dengan username GitHub yang benar
echo.
echo Memperbarui file dengan username GitHub Anda...
powershell -Command "(Get-Content _config.yml) -replace 'username', '%github_username%' | Set-Content _config.yml"
powershell -Command "(Get-Content README.md) -replace 'username', '%github_username%' | Set-Content README.md"
powershell -Command "(Get-Content index.md) -replace 'username', '%github_username%' | Set-Content index.md"
powershell -Command "(Get-Content notebooks\github_pages_demo.ipynb) -replace 'username', '%github_username%' | Set-Content notebooks\github_pages_demo.ipynb"
powershell -Command "(Get-Content GITHUB_SETUP.md) -replace 'your-username', '%github_username%' | Set-Content GITHUB_SETUP.md"

echo.
echo Menginisialisasi repositori git...
git init

echo.
echo Menambahkan semua file ke repositori...
git add -A

echo.
echo Membuat commit awal...
git commit -m "Initial commit with GitHub Pages support"

echo.
echo Langkah selanjutnya:
echo 1. Buat repositori baru di GitHub
echo 2. Jalankan perintah berikut untuk menghubungkan ke repositori GitHub Anda:
echo    git remote add origin https://github.com/%github_username%/face-detection-haar-cascade.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Aktifkan GitHub Pages di pengaturan repositori
echo.

pause
