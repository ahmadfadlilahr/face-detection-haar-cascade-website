#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Program Deteksi Wajah Real-time menggunakan Webcam dan Haar Cascades (LOKAL)
dengan peningkatan akurasi menggunakan multiple cascade classifiers dan preprocessing lanjutan.
Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
"""

import os
import sys

# Penanganan error import
try:
    import cv2
    import numpy as np
    import requests
    import time
except ImportError:
    print("Menginstal dependensi yang diperlukan...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "opencv-python", "numpy", "requests"])
    import cv2
    import numpy as np
    import requests
    import time
    print("Dependensi berhasil diinstal.")

def merge_faces(faces_list):
    """Menggabungkan hasil deteksi wajah dan menghilangkan duplikat"""
    if not faces_list:
        return np.array([])
    
    # Gabungkan semua hasil deteksi
    all_faces = np.vstack(faces_list) if len(faces_list) > 1 else faces_list[0]
    
    # Jika tidak ada wajah yang terdeteksi, kembalikan array kosong
    if len(all_faces) == 0:
        return np.array([])
    
    # Implementasi Non-Maximum Suppression (NMS) sederhana
    # Urutkan wajah berdasarkan area (w*h) dari besar ke kecil
    areas = all_faces[:, 2] * all_faces[:, 3]
    indices = np.argsort(-areas)  # Urutan menurun
    
    # Ambang batas untuk overlap
    overlap_threshold = 0.3
    
    keep = []
    
    for idx in indices:
        keep_face = True
        
        # Kotak yang akan diperiksa
        x1 = all_faces[idx, 0]
        y1 = all_faces[idx, 1]
        x2 = x1 + all_faces[idx, 2]
        y2 = y1 + all_faces[idx, 3]
        area1 = (x2 - x1) * (y2 - y1)
        
        # Bandingkan dengan kotak yang sudah disimpan
        for kept_idx in keep:
            # Kotak yang sudah disimpan
            kx1 = all_faces[kept_idx, 0]
            ky1 = all_faces[kept_idx, 1]
            kx2 = kx1 + all_faces[kept_idx, 2]
            ky2 = ky1 + all_faces[kept_idx, 3]
            area2 = (kx2 - kx1) * (ky2 - ky1)
            
            # Hitung area overlap
            x_overlap = max(0, min(x2, kx2) - max(x1, kx1))
            y_overlap = max(0, min(y2, ky2) - max(y1, ky1))
            overlap_area = x_overlap * y_overlap
            
            # Hitung IoU (Intersection over Union)
            iou = overlap_area / float(area1 + area2 - overlap_area)
            
            if iou > overlap_threshold:
                keep_face = False
                break
        
        if keep_face:
            keep.append(idx)
    
    # Kembalikan wajah yang disimpan
    return all_faces[keep]

def main():
    """Alur Utama Program Deteksi Wajah dari Webcam (LOKAL)"""
    
    print("Selamat Datang di Program Deteksi Wajah Real-time dari Webcam (Lokal)!")

    # Tahap 1: Persiapan Classifier Haar Cascade
    # -----------------------------------------
    cascade_files = {
        'default': 'haarcascade_frontalface_default.xml',
        'alt': 'haarcascade_frontalface_alt.xml',
        'alt2': 'haarcascade_frontalface_alt2.xml',
        'profile': 'haarcascade_profileface.xml'
    }

    # Unduh semua file cascade yang diperlukan
    print("Memeriksa dan mengunduh file cascade...")
    
    for cascade_name, cascade_file in cascade_files.items():
        cascade_url = f'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/{cascade_file}'
        
        if not os.path.exists(cascade_file):
            print(f"File cascade '{cascade_file}' tidak ditemukan, mengunduh...")
            try:
                response = requests.get(cascade_url, timeout=10)
                response.raise_for_status()
                with open(cascade_file, 'wb') as f:
                    f.write(response.content)
                print("Unduhan selesai.")
            except requests.exceptions.RequestException as e:
                print(f"Gagal mengunduh file cascade: {e}")
                if cascade_name == 'default':  # Hanya keluar jika file default yang gagal
                    return
            except Exception as e:
                print(f"Terjadi error lain saat mengunduh: {e}")
                if cascade_name == 'default':  # Hanya keluar jika file default yang gagal
                    return

    # Muat semua klasifikasi cascade
    face_cascade = cv2.CascadeClassifier(cascade_files['default'])
    face_cascade_alt = cv2.CascadeClassifier(cascade_files['alt']) if os.path.exists(cascade_files['alt']) else None
    face_cascade_alt2 = cv2.CascadeClassifier(cascade_files['alt2']) if os.path.exists(cascade_files['alt2']) else None
    profile_cascade = cv2.CascadeClassifier(cascade_files['profile']) if os.path.exists(cascade_files['profile']) else None

    if face_cascade.empty():
        print(f"Error: Gagal memuat file cascade utama '{cascade_files['default']}'.")
        return
    else:
        print(f"Classifier cascade utama berhasil dimuat.")
        
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
        frame_count = 0
        enhanced_detection_interval = 10  # Setiap berapa frame akan menggunakan deteksi yang lebih akurat
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Gagal membaca frame dari webcam. Menghentikan...")
                break

            # Untuk kecepatan, hitung frame dan hanya lakukan deteksi yang intensif pada interval tertentu
            frame_count += 1
            use_enhanced_detection = (frame_count % enhanced_detection_interval == 0)
            
            # Pra-pemrosesan gambar
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame_equalized = cv2.equalizeHist(gray_frame)
            
            # Tambahkan CLAHE untuk peningkatan kontras adaptif jika dibutuhkan
            if use_enhanced_detection:
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                gray_frame_enhanced = clahe.apply(gray_frame_equalized)
                # Tambahkan filter bilateral untuk mengurangi noise
                gray_frame_enhanced = cv2.bilateralFilter(gray_frame_enhanced, 9, 75, 75)
            else:
                gray_frame_enhanced = gray_frame_equalized

            all_faces_detected = []
            
            # Untuk kecepatan, gunakan deteksi dasar pada sebagian besar frame
            if not use_enhanced_detection:
                # Deteksi wajah standar dengan cascade default untuk kecepatan
                faces = face_cascade.detectMultiScale(
                    gray_frame_enhanced,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(50, 50)
                )
                if len(faces) > 0:
                    all_faces_detected.append(faces)
            else:
                # Pada interval tertentu, lakukan deteksi yang lebih menyeluruh
                # Deteksi dengan cascade default
                faces_default = face_cascade.detectMultiScale(
                    gray_frame_enhanced,
                    scaleFactor=1.08,
                    minNeighbors=4,
                    minSize=(30, 30)
                )
                if len(faces_default) > 0:
                    all_faces_detected.append(faces_default)
                
                # Deteksi dengan cascade alternatif
                if face_cascade_alt is not None:
                    faces_alt = face_cascade_alt.detectMultiScale(
                        gray_frame_enhanced,
                        scaleFactor=1.08,
                        minNeighbors=3,
                        minSize=(30, 30)
                    )
                    if len(faces_alt) > 0:
                        all_faces_detected.append(faces_alt)
                    
                # Deteksi dengan cascade alternatif 2
                if face_cascade_alt2 is not None:
                    faces_alt2 = face_cascade_alt2.detectMultiScale(
                        gray_frame_enhanced,
                        scaleFactor=1.1,
                        minNeighbors=4,
                        minSize=(35, 35)
                    )
                    if len(faces_alt2) > 0:
                        all_faces_detected.append(faces_alt2)
                
                # Deteksi profil jika dibutuhkan ekstra akurasi
                if len(all_faces_detected) == 0 and profile_cascade is not None:
                    profile_faces = profile_cascade.detectMultiScale(
                        gray_frame_enhanced,
                        scaleFactor=1.1,
                        minNeighbors=3,
                        minSize=(35, 35)
                    )
                    if len(profile_faces) > 0:
                        all_faces_detected.append(profile_faces)
                    
                    # Flip gambar secara horizontal untuk mendeteksi profil dari sisi lain
                    flipped_frame = cv2.flip(gray_frame_enhanced, 1)
                    flipped_profile_faces = profile_cascade.detectMultiScale(
                        flipped_frame,
                        scaleFactor=1.1,
                        minNeighbors=3,
                        minSize=(35, 35)
                    )
                    
                    # Konversi koordinat flip kembali ke koordinat original
                    if len(flipped_profile_faces) > 0:
                        width = gray_frame_enhanced.shape[1]
                        for i, (x, y, w, h) in enumerate(flipped_profile_faces):
                            flipped_profile_faces[i][0] = width - x - w
                        all_faces_detected.append(flipped_profile_faces)

            # Gabungkan dan hapus wajah duplikat
            if all_faces_detected:
                merged_faces = merge_faces(all_faces_detected)
                num_faces = len(merged_faces)
                
                # Gambar kotak di sekitar wajah yang terdeteksi
                for (x, y, w, h) in merged_faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                num_faces = 0
                
            # Tampilkan informasi jumlah wajah terdeteksi
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
