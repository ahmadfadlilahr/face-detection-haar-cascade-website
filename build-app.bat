@echo off
echo Mempersiapkan aplikasi Deteksi Wajah untuk distribusi...
echo Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
echo.

REM Direktori untuk build
set BUILD_DIR=dist

REM Pastikan direktori build ada
if not exist %BUILD_DIR% mkdir %BUILD_DIR%

REM Copy file-file yang diperlukan
echo Menyalin file-file aplikasi...
xcopy /Y /E /I src %BUILD_DIR%\src
xcopy /Y /E /I templates %BUILD_DIR%\templates
xcopy /Y start-web-app.bat %BUILD_DIR%\
xcopy /Y start-desktop-app.bat %BUILD_DIR%\
xcopy /Y requirements.txt %BUILD_DIR%\
xcopy /Y README.md %BUILD_DIR%\
xcopy /Y README_ID.md %BUILD_DIR%\
xcopy /Y .env.example %BUILD_DIR%\
xcopy /Y LICENSE %BUILD_DIR%\
xcopy /Y /E /I docs %BUILD_DIR%\docs

REM Buat file setup_app.bat dalam direktori build
echo @echo off > %BUILD_DIR%\setup_app.bat
echo echo Mempersiapkan aplikasi Deteksi Wajah dengan Haar Cascade... >> %BUILD_DIR%\setup_app.bat
echo echo Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah) >> %BUILD_DIR%\setup_app.bat
echo echo. >> %BUILD_DIR%\setup_app.bat
echo echo Menginstal dependensi... >> %BUILD_DIR%\setup_app.bat
echo pip install -r requirements.txt >> %BUILD_DIR%\setup_app.bat
echo. >> %BUILD_DIR%\setup_app.bat
echo if not exist .env copy .env.example .env >> %BUILD_DIR%\setup_app.bat
echo echo. >> %BUILD_DIR%\setup_app.bat
echo echo Persiapan selesai! Anda dapat menjalankan aplikasi dengan: >> %BUILD_DIR%\setup_app.bat
echo echo - start-desktop-app.bat untuk aplikasi desktop >> %BUILD_DIR%\setup_app.bat
echo echo - start-web-app.bat untuk aplikasi web >> %BUILD_DIR%\setup_app.bat
echo. >> %BUILD_DIR%\setup_app.bat
echo pause >> %BUILD_DIR%\setup_app.bat

echo.
echo Proses build selesai. File-file distribusi tersedia di folder '%BUILD_DIR%'.
echo.
echo Distribusikan folder '%BUILD_DIR%' kepada pengguna dan minta mereka menjalankan 'setup_app.bat' terlebih dahulu.
echo.

pause
