# Documentation

*Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)*

## Overview

This application provides real-time face detection using OpenCV's Haar Cascade classifiers. The detection is performed on a live video feed from a webcam.

## How it Works

1. **Haar Cascade Loading**: 
   - The application loads a pre-trained Haar Cascade classifier for face detection
   - If the classifier file is not found locally, it automatically downloads it from the OpenCV GitHub repository

2. **Webcam Initialization**: 
   - The application attempts to initialize the webcam using the default method
   - If that fails, it tries an alternative method using CAP_DSHOW

3. **Face Detection Process**:
   - Each frame from the webcam is:
     - Converted to grayscale
     - Enhanced with histogram equalization
     - Processed with the Haar Cascade classifier to detect faces
   - Detected faces are outlined with rectangles
   - A counter displays the number of faces detected in real-time

4. **Termination**:
   - The application is terminated when the 'q' key is pressed
   - Resources are properly released upon termination

## Parameters

The face detection parameters can be adjusted for better performance:

- `scaleFactor`: How much the image size is reduced at each image scale (default: 1.1)
- `minNeighbors`: How many neighbors each candidate rectangle should have to retain it (default: 7)
- `minSize`: Minimum possible object size (default: 50x50 pixels)

## Troubleshooting

If the application fails to detect faces properly, try:

1. Adjusting lighting conditions to ensure better contrast
2. Adjusting the `scaleFactor` and `minNeighbors` parameters
3. Ensuring your webcam is working correctly

## Extensions

Possible extensions to this project:
1. Face recognition capabilities
2. Emotion detection
3. Eye detection
4. Recording functionality
5. Multiple camera support
