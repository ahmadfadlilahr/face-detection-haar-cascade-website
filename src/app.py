#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aplikasi Web untuk Deteksi Wajah dengan Haar Cascade
Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
"""

import os
import sys
import base64
from io import BytesIO
import threading
import time

# Penanganan error import
try:
    import cv2
    import numpy as np
    from flask import Flask, render_template, Response, request, jsonify
    import requests
except ImportError:
    print("Menginstal dependensi yang diperlukan...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                         "opencv-python", "numpy", "flask", "requests"])
    import cv2
    import numpy as np
    from flask import Flask, render_template, Response, request, jsonify
    import requests
    print("Dependensi berhasil diinstal.")

app = Flask(__name__)

# Variabel global
camera = None
output_frame = None
lock = threading.Lock()
face_cascade = None
face_cascade_alt = None
face_cascade_alt2 = None
profile_cascade = None
detection_running = False

def download_cascade_if_needed():
    """Download file cascade jika belum ada"""
    global face_cascade, face_cascade_alt, face_cascade_alt2, profile_cascade
    
    # Menggunakan haarcascade_frontalface_default.xml sebagai cascade utama
    cascade_filename = 'haarcascade_frontalface_default.xml'
    cascade_url = f'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/{cascade_filename}'

    if not os.path.exists(cascade_filename):
        print(f"File cascade '{cascade_filename}' tidak ditemukan, mengunduh...")
        try:
            response = requests.get(cascade_url, timeout=10)
            response.raise_for_status()
            with open(cascade_filename, 'wb') as f:
                f.write(response.content)
            print("Unduhan selesai.")
        except Exception as e:
            print(f"Gagal mengunduh file cascade: {e}")
            return False
    
    # Unduh file cascade tambahan untuk meningkatkan akurasi
    cascade_files = {
        'haarcascade_frontalface_alt.xml': 'face_cascade_alt',
        'haarcascade_frontalface_alt2.xml': 'face_cascade_alt2',
        'haarcascade_profileface.xml': 'profile_cascade'
    }
    
    for filename, var_name in cascade_files.items():
        if not os.path.exists(filename):
            url = f'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/{filename}'
            print(f"Mengunduh file cascade tambahan: {filename}...")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Unduhan {filename} selesai.")
            except Exception as e:
                print(f"Gagal mengunduh file cascade: {e}")
                # Lanjutkan meskipun gagal mengunduh file tambahan
    
    # Muat semua cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_cascade_alt = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    face_cascade_alt2 = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
    
    if face_cascade.empty():
        print(f"Error: Gagal memuat file cascade utama.")
        return False
    else:
        print(f"Semua classifier cascade berhasil dimuat.")
        return True
    
# Fungsi untuk menggabungkan hasil dari beberapa deteksi wajah dan menghilangkan duplikat
def merge_faces(faces_list):
    """Menggabungkan hasil deteksi wajah dan menghilangkan duplikat"""
    if not faces_list:
        return np.array([])
    
    # Gabungkan semua hasil deteksi
    all_faces = np.vstack(faces_list) if len(faces_list) > 1 else faces_list[0]
    
    # Jika tidak ada wajah yang terdeteksi, kembalikan array kosong
    if len(all_faces) == 0:
        return np.array([])
    
    # Konversi format ke [x, y, w, h]
    result_faces = []
    
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

def init_camera():
    """Inisialisasi kamera"""
    global camera
    
    print("Menginisialisasi webcam...")
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Tidak bisa membuka webcam dengan metode default.")
        print("Mencoba membuka webcam dengan backend alternatif (CAP_DSHOW)...")
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not camera.isOpened():
            print("Error: Tetap tidak bisa membuka webcam. Pastikan webcam terpasang dan tidak digunakan aplikasi lain.")
            return False
        else:
            print("Webcam berhasil dibuka dengan backend CAP_DSHOW.")
    else:
        print("Webcam berhasil dibuka dengan metode default.")
    
    return True

def detect_faces():
    """Deteksi wajah dari webcam secara real-time dengan akurasi yang ditingkatkan"""
    global camera, output_frame, lock, face_cascade, face_cascade_alt, face_cascade_alt2, profile_cascade, detection_running
    
    num_faces = 0
    frame_count = 0
    enhanced_detection_interval = 10  # Setiap berapa frame akan menggunakan deteksi yang lebih akurat
    
    while detection_running:
        success, frame = camera.read()
        if not success:
            print("Gagal membaca frame dari webcam.")
            break
        
        # Untuk kecepatan, hitung frame dan hanya lakukan deteksi yang intensif pada interval tertentu
        frame_count += 1
        use_enhanced_detection = (frame_count % enhanced_detection_interval == 0)
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Pra-pemrosesan gambar
        gray_frame_equalized = cv2.equalizeHist(gray_frame)
        
        all_faces_detected = []
        
        # Untuk kecepatan, gunakan deteksi dasar pada sebagian besar frame
        if not use_enhanced_detection:
            # Deteksi wajah standar dengan cascade default untuk kecepatan
            faces = face_cascade.detectMultiScale(
                gray_frame_equalized,
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
                gray_frame_equalized,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            if len(faces_default) > 0:
                all_faces_detected.append(faces_default)
            
            # Deteksi dengan cascade alternatif
            faces_alt = face_cascade_alt.detectMultiScale(
                gray_frame_equalized,
                scaleFactor=1.1,
                minNeighbors=4,
                minSize=(30, 30)
            )
            if len(faces_alt) > 0:
                all_faces_detected.append(faces_alt)
            
            # Deteksi profil jika dibutuhkan ekstra akurasi
            if len(all_faces_detected) == 0:
                profile_faces = profile_cascade.detectMultiScale(
                    gray_frame_equalized,
                    scaleFactor=1.1,
                    minNeighbors=3,
                    minSize=(35, 35)
                )
                if len(profile_faces) > 0:
                    all_faces_detected.append(profile_faces)
        
        # Gabungkan dan hapus wajah duplikat
        if all_faces_detected:
            # Gabungkan hasil deteksi dan filter duplikat
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
        
        # Update frame output
        with lock:
            output_frame = frame.copy()

def generate_frames():
    """Generator untuk streaming frame ke halaman web"""
    global output_frame, lock
    
    while True:
        with lock:
            if output_frame is None:
                continue
            
            # Encode frame sebagai JPEG
            (flag, encoded_image) = cv2.imencode(".jpg", output_frame)
            
            if not flag:
                continue
                
        # Yield hasil sebagai respons streaming
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
              bytearray(encoded_image) + b'\r\n')

@app.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Streaming video feed untuk halaman web"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    """Memulai deteksi wajah"""
    global detection_running
    
    if not detection_running:
        # Inisialisasi cascade classifier jika belum
        if face_cascade is None:
            if not download_cascade_if_needed():
                return jsonify({"success": False, "message": "Gagal memuat cascade classifier"})
        
        # Inisialisasi kamera jika belum
        if camera is None:
            if not init_camera():
                return jsonify({"success": False, "message": "Gagal menginisialisasi kamera"})
        
        detection_running = True
        threading.Thread(target=detect_faces).start()
        return jsonify({"success": True, "message": "Deteksi wajah dimulai"})
    else:
        return jsonify({"success": False, "message": "Deteksi wajah sudah berjalan"})

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    """Menghentikan deteksi wajah"""
    global detection_running, camera
    
    detection_running = False
    
    # Tunggu thread deteksi wajah berhenti
    time.sleep(1)
    
    # Reset kamera
    if camera is not None:
        camera.release()
        camera = None
    
    return jsonify({"success": True, "message": "Deteksi wajah dihentikan"})

@app.route('/upload', methods=['POST'])
def upload_image():
    """Deteksi wajah dari gambar yang diunggah dengan akurasi yang sangat ditingkatkan"""
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "Tidak ada file yang diunggah"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"success": False, "message": "Tidak ada file yang dipilih"})
    
    # Baca gambar yang diunggah
    image_stream = file.read()
    nparr = np.frombuffer(image_stream, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Inisialisasi cascade classifier jika belum
    if face_cascade is None:
        if not download_cascade_if_needed():
            return jsonify({"success": False, "message": "Gagal memuat cascade classifier"})
    
    # Pra-pemrosesan gambar yang ditingkatkan
    original_image = image.copy()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 1. Ekualisasi histogram
    gray_image_equalized = cv2.equalizeHist(gray_image)
    
    # 2. Penerapan filter bilateral untuk mengurangi noise dengan tetap mempertahankan tepi
    filtered_image = cv2.bilateralFilter(gray_image_equalized, 9, 75, 75)
    
    # 3. Peningkatan kontras adaptif dengan CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(filtered_image)
    
    # 4. Normalisasi gambar
    normalized_image = cv2.normalize(enhanced_image, None, alpha=0, beta=255, 
                                    norm_type=cv2.NORM_MINMAX)
    
    # Daftar untuk menyimpan hasil deteksi wajah dari berbagai classifier
    all_faces_detected = []
    
    # Deteksi menggunakan cascade default dengan parameter yang berbeda
    faces_default_sensitive = face_cascade.detectMultiScale(
        enhanced_image,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces_default_sensitive) > 0:
        all_faces_detected.append(faces_default_sensitive)
    
    # Deteksi menggunakan cascade alt
    faces_alt = face_cascade_alt.detectMultiScale(
        enhanced_image,
        scaleFactor=1.08,
        minNeighbors=3,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces_alt) > 0:
        all_faces_detected.append(faces_alt)
    
    # Deteksi menggunakan cascade alt2
    faces_alt2 = face_cascade_alt2.detectMultiScale(
        enhanced_image, 
        scaleFactor=1.08,
        minNeighbors=4,
        minSize=(35, 35),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces_alt2) > 0:
        all_faces_detected.append(faces_alt2)
    
    # Deteksi wajah profil (dari samping)
    # Deteksi wajah dari kiri ke kanan
    profile_faces = profile_cascade.detectMultiScale(
        enhanced_image,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(profile_faces) > 0:
        all_faces_detected.append(profile_faces)
    
    # Flip gambar secara horizontal dan deteksi profil lagi (untuk wajah dari sisi lain)
    flipped_image = cv2.flip(enhanced_image, 1)
    flipped_profile_faces = profile_cascade.detectMultiScale(
        flipped_image,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    # Konversi koordinat wajah pada gambar flipped kembali ke koordinat di gambar asli
    if len(flipped_profile_faces) > 0:
        width = enhanced_image.shape[1]
        for i, (x, y, w, h) in enumerate(flipped_profile_faces):
            flipped_profile_faces[i][0] = width - x - w  # Menyesuaikan koordinat x
        all_faces_detected.append(flipped_profile_faces)
    
    # Jika masih belum ada wajah terdeteksi, coba dengan gambar asli yang dinormalisasi
    if len(all_faces_detected) == 0:
        faces_normalized = face_cascade.detectMultiScale(
            normalized_image,
            scaleFactor=1.05,
            minNeighbors=2,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces_normalized) > 0:
            all_faces_detected.append(faces_normalized)
    
    # Jika masih belum ada wajah terdeteksi, coba dengan gambar asli (gray)
    if len(all_faces_detected) == 0:
        faces_original = face_cascade.detectMultiScale(
            gray_image,
            scaleFactor=1.05,
            minNeighbors=2,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces_original) > 0:
            all_faces_detected.append(faces_original)
    
    # Gabungkan dan hapus wajah duplikat
    if all_faces_detected:
        merged_faces = merge_faces(all_faces_detected)
        num_faces = len(merged_faces)
    else:
        merged_faces = np.array([])
        num_faces = 0
    
    # Gambar kotak di sekitar wajah yang terdeteksi pada gambar asli
    for (x, y, w, h) in merged_faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Tambahkan indikator confidence untuk warna bingkai (opsional)
        # Semakin tinggi confidence, semakin hijau warnanya
        # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Tampilkan jumlah wajah yang terdeteksi
    text_position = (10, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 0, 0)  # Biru
    thickness = 2
    line_type = cv2.LINE_AA

    cv2.putText(image, f'Wajah Terdeteksi: {num_faces}',
                text_position,
                font,
                font_scale,
                font_color,
                thickness,
                line_type)
    
    # Konversi gambar hasil deteksi ke base64 untuk ditampilkan di halaman web
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify({
        "success": True,
        "message": f"{num_faces} wajah terdeteksi",
        "image": image_base64
    })

if __name__ == '__main__':
    app.run(debug=True)
