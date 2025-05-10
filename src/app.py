#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aplikasi Web untuk Deteksi Wajah dengan Haar Cascade
Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
"""

import os
import cv2
import numpy as np
import base64
from flask import Flask, render_template, Response, request, jsonify
import threading
import time
import requests
from io import BytesIO

app = Flask(__name__)

# Variabel global
camera = None
output_frame = None
lock = threading.Lock()
face_cascade = None
detection_running = False

def download_cascade_if_needed():
    """Download file cascade jika belum ada"""
    global face_cascade
    
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
    
    face_cascade = cv2.CascadeClassifier(cascade_filename)
    
    if face_cascade.empty():
        print(f"Error: Gagal memuat file cascade '{cascade_filename}'.")
        return False
    else:
        print(f"Classifier cascade '{cascade_filename}' berhasil dimuat.")
        return True

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
    """Deteksi wajah dari webcam secara real-time"""
    global camera, output_frame, lock, face_cascade, detection_running
    
    num_faces = 0
    
    while detection_running:
        success, frame = camera.read()
        if not success:
            print("Gagal membaca frame dari webcam.")
            break
            
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame_equalized = cv2.equalizeHist(gray_frame)
        
        faces = face_cascade.detectMultiScale(
            gray_frame_equalized,
            scaleFactor=1.1,
            minNeighbors=7,
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
    """Deteksi wajah dari gambar yang diunggah"""
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
    
    # Deteksi wajah
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image_equalized = cv2.equalizeHist(gray_image)
    
    faces = face_cascade.detectMultiScale(
        gray_image_equalized,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(50, 50)
    )
    
    num_faces = len(faces)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
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
