#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for web application face detection functionality
Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import base64

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestWebAppFunctions(unittest.TestCase):
    """Test cases for the web application face detection"""

    @patch('src.app.cv2')
    @patch('src.app.face_cascade')
    def test_detect_faces_in_image(self, mock_face_cascade, mock_cv2):
        """Test face detection in an uploaded image"""
        from src.app import upload_image
        from flask import Flask
        
        app = Flask(__name__)
        with app.test_request_context():
            # Setup mocks
            mock_file = MagicMock()
            mock_file.filename = 'test.jpg'
            mock_file.read.return_value = b'test_image_data'
            
            # Mock requests.files to return our mock file
            with patch('src.app.request') as mock_request:
                mock_request.files = {'file': mock_file}
                
                # Mock numpy and cv2 operations
                mock_cv2.imdecode.return_value = MagicMock()
                mock_cv2.cvtColor.return_value = MagicMock()
                mock_cv2.equalizeHist.return_value = MagicMock()
                
                # Setup face detection mock to return one face
                mock_face_cascade.detectMultiScale.return_value = [(10, 10, 100, 100)]
                
                # Mock imencode to return success and encoded image
                mock_cv2.imencode.return_value = (True, b'encoded_image')
                
                # Patch base64.b64encode
                with patch('base64.b64encode') as mock_b64encode:
                    mock_b64encode.return_value = b'base64_encoded_image'
                    
                    # Call the function
                    result = upload_image()
                    
                    # Verify the result
                    data = result.get_json()
                    self.assertTrue(data['success'])
                    self.assertEqual(data['message'], "1 wajah terdeteksi")
                    self.assertEqual(data['image'], 'base64_encoded_image')
    
    @patch('src.app.cv2')
    @patch('src.app.face_cascade')
    @patch('src.app.threading')
    def test_start_detection(self, mock_threading, mock_face_cascade, mock_cv2):
        """Test starting face detection"""
        from src.app import start_detection, download_cascade_if_needed, init_camera
        from flask import Flask
        
        # Set up patch for download_cascade_if_needed to return True
        with patch('src.app.download_cascade_if_needed', return_value=True):
            # Set up patch for init_camera to return True
            with patch('src.app.init_camera', return_value=True):
                app = Flask(__name__)
                with app.test_request_context():
                    with patch('src.app.detection_running', False):
                        with patch('src.app.face_cascade', None):
                            # Call the function
                            result = start_detection()
                            
                            # Verify result
                            data = result.get_json()
                            self.assertTrue(data['success'])
                            self.assertEqual(data['message'], "Deteksi wajah dimulai")

if __name__ == '__main__':
    unittest.main()
