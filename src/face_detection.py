#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Program Deteksi Wajah Real-time menggunakan Webcam dan Haar Cascades (LOKAL)
dengan tambahan informasi jumlah wajah terdeteksi dan ekualisasi histogram.
Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
"""

import cv2
import numpy as np
import os
import requests
import time

def main():
    """Alur Utama Program Deteksi Wajah dari Webcam (LOKAL)"""
    
    print("Selamat Datang di Program Deteksi Wajah Real-time dari Webcam (Lokal)!")

    # Tahap 1: Persiapan Classifier Haar Cascade
    # -----------------------------------------
    cascade_filename = 'haarcascade_frontalface_default.xml'  # Anda bisa coba ganti dengan _alt.xml atau _alt2.xml
    cascade_url = f'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/{cascade_filename}'

    if not os.path.exists(cascade_filename):
        print(f"File cascade '{cascade_filename}' tidak ditemukan, mengunduh...")
        try:
            response = requests.get(cascade_url, timeout=10)
            response.raise_for_status()
            with open(cascade_filename, 'wb') as f:
                f.write(response.content)
            print("Unduhan selesai.")
        except requests.exceptions.RequestException as e:
            print(f"Gagal mengunduh file cascade: {e}")
            return
        except Exception as e:
            print(f"Terjadi error lain saat mengunduh: {e}")
            return

    face_cascade = cv2.CascadeClassifier(cascade_filename)

    if face_cascade.empty():
        print(f"Error: Gagal memuat file cascade '{cascade_filename}'.")
        return
    else:
        print(f"Classifier cascade '{cascade_filename}' berhasil dimuat.")

    # Tahap 2: Inisialisasi Webcam
    # -----------------------------
    print("Menginisialisasi webcam...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Tidak bisa membuka webcam dengan metode default.")
        print("Mencoba membuka webcam dengan backend alternatif (CAP_DSHOW)...")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("Error: Tetap tidak bisa membuka webcam dengan backend alternatif. Pastikan webcam terpasang dan tidak digunakan aplikasi lain.")
            return
        else:
            print("Webcam berhasil dibuka dengan backend CAP_DSHOW.")
    else:
        print("Webcam berhasil dibuka dengan metode default.")

    print("\n--- Memulai Deteksi Wajah dari Webcam (Lokal) ---")
    print("Tekan tombol 'q' pada jendela video untuk keluar.")

    # Tahap 3: Loop Utama untuk Deteksi Real-time
    # -------------------------------------------
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Gagal membaca frame dari webcam. Menghentikan...")
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # **PENINGKATAN: Terapkan Ekualisasi Histogram**
            # Ini dapat membantu dalam kondisi pencahayaan yang bervariasi atau kurang kontras
            gray_frame_equalized = cv2.equalizeHist(gray_frame)

            # Gunakan frame yang sudah diekualisasi untuk deteksi
            faces = face_cascade.detectMultiScale(
                gray_frame_equalized,  # << Gunakan frame yang sudah dipra-pemrosesan
                scaleFactor=1.1,       # Mungkin perlu penyesuaian setelah ekualisasi
                minNeighbors=7,        # Mungkin perlu penyesuaian setelah ekualisasi
                minSize=(50, 50)
            )

            num_faces = len(faces)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            text_position = (10, 30)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_color = (255, 0, 0)  # Biru
            thickness = 2
            line_type = cv2.LINE_AA

            cv2.putText(frame, f'Wajah Terdeteksi: {num_faces}',
                        text_position,
                        font,
                        font_scale,
                        font_color,
                        thickness,
                        line_type)
            
            # Jika Anda ingin melihat frame grayscale yang diekualisasi (untuk debugging/pemahaman):
            # cv2.imshow('Grayscale Equalized', gray_frame_equalized)

            cv2.imshow('Deteksi Wajah Real-time', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Tombol 'q' ditekan, keluar dari loop...")
                break
            try:
                if cv2.getWindowProperty('Deteksi Wajah Real-time', cv2.WND_PROP_VISIBLE) < 1:
                    print("Jendela tampilan ditutup, keluar dari loop...")
                    break
            except cv2.error:
                print("Error saat memeriksa properti jendela (mungkin sudah ditutup). Keluar dari loop...")
                break

    except Exception as e:
        print(f"Terjadi error selama eksekusi loop utama: {e}")
    finally:
        # Tahap 4: Pembersihan
        # --------------------
        print("Melepaskan webcam dan menutup jendela...")
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        time.sleep(0.5)
        print("\nProgram Selesai.")

if __name__ == "__main__":
    main()
