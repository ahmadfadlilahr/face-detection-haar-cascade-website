"""
Face Detection with Haar Cascade - Setup
Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
"""

from setuptools import setup, find_packages

setup(    name="face-detection-haar-cascade",
    version="0.2.0",
    description="Real-time face detection using Haar Cascade classifiers",
    author="Ahmad Fadlilah",
    author_email="ahmad.fadlilah@example.com",
    url="https://github.com/ahmadfadlilah/face-detection-haar-cascade",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.20.0",
        "requests>=2.25.0",
    ],
    python_requires=">=3.6",
)
