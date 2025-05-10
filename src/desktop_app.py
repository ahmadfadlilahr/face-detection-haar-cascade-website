#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aplikasi Desktop untuk Menjalankan Deteksi Wajah dengan Web Interface
Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import webbrowser
import subprocess
import time

class FaceDetectionApp(tk.Tk):    def __init__(self):
        super().__init__()
        self.title("Deteksi Wajah dengan Haar Cascade")
        self.geometry("500x400")
        self.configure(bg="#f0f0f0")
        
        self.server_process = None
        self.server_running = False
        
        # Tampilkan copyright di konsol saat aplikasi dijalankan
        print("Deteksi Wajah dengan Haar Cascade")
        print("Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)")
        print("-" * 70)
        
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg="#343a40", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame, 
            text="Deteksi Wajah dengan Haar Cascade", 
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#343a40"
        )
        title_label.pack()
        
        # Main content
        content_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Aplikasi Web
        web_frame = tk.LabelFrame(
            content_frame, 
            text="Aplikasi Web", 
            padx=10, 
            pady=10,
            bg="#f0f0f0",
            font=("Arial", 12)
        )
        web_frame.pack(fill=tk.X, pady=10)
        
        web_desc = tk.Label(
            web_frame, 
            text="Jalankan aplikasi web untuk deteksi wajah\n"
                 "dengan antarmuka web yang lengkap.",
            bg="#f0f0f0",
            justify=tk.LEFT
        )
        web_desc.pack(anchor=tk.W)
        
        button_frame = tk.Frame(web_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = tk.Button(
            button_frame, 
            text="Mulai Server Web", 
            command=self.start_web_server,
            bg="#0d6efd",
            fg="white",
            padx=10,
            pady=5,
            font=("Arial", 10),
            width=15
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame, 
            text="Berhenti", 
            command=self.stop_web_server,
            bg="#dc3545",
            fg="white",
            padx=10,
            pady=5,
            font=("Arial", 10),
            width=10,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.open_browser_button = tk.Button(
            button_frame, 
            text="Buka Browser", 
            command=self.open_browser,
            bg="#198754",
            fg="white",
            padx=10,
            pady=5,
            font=("Arial", 10),
            width=15,
            state=tk.DISABLED
        )
        self.open_browser_button.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_frame = tk.Frame(self, bg="#f8f9fa", padx=10, pady=5)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            self.status_frame, 
            text="Siap", 
            bg="#f8f9fa",
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(
            self.status_frame, 
            mode="indeterminate", 
            length=150
        )
    
    def start_web_server(self):
        if self.server_running:
            messagebox.showinfo("Info", "Server web sudah berjalan.")
            return
        
        self.set_status("Memulai server web...")
        self.progress_bar.pack(side=tk.RIGHT, padx=10)
        self.progress_bar.start(10)
        
        # Cari file app.py
        app_dir = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(app_dir, 'app.py')
        
        if not os.path.exists(app_path):
            # Coba cari di direktori src
            app_path = os.path.join(app_dir, '..', 'src', 'app.py')
            if not os.path.exists(app_path):
                self.set_status("Error: File app.py tidak ditemukan")
                messagebox.showerror("Error", "File aplikasi web (app.py) tidak ditemukan.")
                self.progress_bar.stop()
                self.progress_bar.pack_forget()
                return
        
        # Jalankan server di thread terpisah
        server_thread = threading.Thread(target=self._run_server, args=(app_path,))
        server_thread.daemon = True
        server_thread.start()
        
        # Tunggu sebentar hingga server berjalan
        time.sleep(2)
        
        self.server_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.open_browser_button.config(state=tk.NORMAL)
        
        self.set_status("Server web sedang berjalan di http://127.0.0.1:5000")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
    
    def _run_server(self, app_path):
        try:
            self.server_process = subprocess.Popen(
                [sys.executable, app_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.server_process.wait()
        except Exception as e:
            self.set_status(f"Error: {str(e)}")
    
    def stop_web_server(self):
        if not self.server_running:
            return
        
        self.set_status("Menghentikan server web...")
        
        if self.server_process:
            if sys.platform.startswith('win'):
                # Windows
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.server_process.pid)])
            else:
                # Linux/Mac
                self.server_process.terminate()
            
            self.server_process = None
        
        self.server_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.open_browser_button.config(state=tk.DISABLED)
        
        self.set_status("Server web dihentikan")
    
    def open_browser(self):
        webbrowser.open("http://127.0.0.1:5000", new=2)
    
    def set_status(self, message):
        self.status_label.config(text=message)
    
    def on_closing(self):
        if self.server_running:
            if messagebox.askyesno("Konfirmasi", "Server web masih berjalan. Hentikan dan keluar?"):
                self.stop_web_server()
                self.destroy()
        else:
            self.destroy()

if __name__ == "__main__":
    app = FaceDetectionApp()
    app.mainloop()
