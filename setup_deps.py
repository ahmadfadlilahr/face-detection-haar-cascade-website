#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk menginstal dependensi yang diperlukan
Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
"""

import os
import sys
import subprocess

def install_dependencies():
    """Menginstal dependensi yang diperlukan untuk aplikasi deteksi wajah"""
    print("Menginstal dependensi yang diperlukan...")
    
    packages = [
        "opencv-python",
        "numpy",
        "requests",
        "flask"
    ]
    
    # Instal semua package yang diperlukan
    for package in packages:
        print(f"Menginstal {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # Verifikasi instalasi
    try:
        import cv2
        import numpy as np
        import requests
        from flask import Flask
        
        print("\nSemua dependensi berhasil diinstal!")
        print("opencv-python:", cv2.__version__)
        print("numpy:", np.__version__)
        print("requests:", requests.__version__)
        print("flask:", Flask.__version__)
    except ImportError as e:
        print(f"\nTerjadi kesalahan saat memverifikasi instalasi: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Script Instalasi Dependensi Deteksi Wajah")
    print("Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)")
    print("-" * 70)
    
    if install_dependencies():
        print("\nSiap untuk menjalankan aplikasi!")
        print("Gunakan salah satu cara berikut:")
        print("1. start-web-app.bat untuk aplikasi web")
        print("2. start-desktop-app.bat untuk aplikasi desktop")
        print("3. notebooks/deteksi_lokal.ipynb untuk deteksi lokal menggunakan notebook")
    else:
        print("\nGagal menginstal dependensi. Silakan coba instal secara manual:")
        print("pip install opencv-python numpy requests flask")
