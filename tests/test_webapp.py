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
import numpy as np

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestWebAppFunctions(unittest.TestCase):
    """Test cases for the web application face detection"""

    @patch('src.app.cv2')
    @patch('src.app.face_cascade')
    @patch('src.app.face_cascade_alt')
    @patch('src.app.face_cascade_alt2')
    @patch('src.app.profile_cascade')
    @patch('src.app.merge_faces')
    def test_detect_faces_in_image(self, mock_merge_faces, mock_profile_cascade, 
                                   mock_face_cascade_alt2, mock_face_cascade_alt, 
                                   mock_face_cascade, mock_cv2):
        """Test face detection in an uploaded image with multiple cascade classifiers"""
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
                mock_cv2.bilateralFilter.return_value = MagicMock()
                mock_cv2.createCLAHE.return_value.apply.return_value = MagicMock()
                mock_cv2.normalize.return_value = MagicMock()
                mock_cv2.flip.return_value = MagicMock()
                
                # Setup multiple face detection mocks
                mock_faces_default = np.array([[10, 10, 100, 100]])
                mock_faces_alt = np.array([[20, 20, 80, 80]])
                mock_faces_alt2 = np.array([[30, 30, 70, 70]])
                mock_profile_faces = np.array([[40, 40, 60, 60]])
                
                mock_face_cascade.detectMultiScale.return_value = mock_faces_default
                mock_face_cascade_alt.detectMultiScale.return_value = mock_faces_alt
                mock_face_cascade_alt2.detectMultiScale.return_value = mock_faces_alt2
                mock_profile_cascade.detectMultiScale.return_value = mock_profile_faces
                
                # Mock merged faces result
                mock_merged_faces = np.array([[15, 15, 90, 90], [35, 35, 65, 65]])
                mock_merge_faces.return_value = mock_merged_faces
                
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
                    self.assertEqual(data['message'], "2 wajah terdeteksi")  # Sesuai dengan jumlah wajah di mock_merged_faces
                    self.assertEqual(data['image'], 'base64_encoded_image')
                    
                    # Verify that all cascade classifiers were called
                    mock_face_cascade.detectMultiScale.assert_called()
                    mock_face_cascade_alt.detectMultiScale.assert_called()
                    mock_face_cascade_alt2.detectMultiScale.assert_called()
                    mock_profile_cascade.detectMultiScale.assert_called()
                    
                    # Verify that merge_faces was called
                    mock_merge_faces.assert_called()
    
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
    
    @patch('src.app.np')
    def test_merge_faces(self, mock_np):
        """Test the merge_faces function that combines multiple detection results"""
        from src.app import merge_faces
        
        # Set up test data
        face1 = np.array([[10, 10, 50, 50]])
        face2 = np.array([[60, 60, 50, 50]])
        face3 = np.array([[12, 12, 48, 48]])  # Similar to face1, should be filtered out
        
        faces_list = [face1, face2, face3]
        
        # Mock numpy operations
        mock_np.vstack.return_value = np.array([[10, 10, 50, 50], [60, 60, 50, 50], [12, 12, 48, 48]])
        mock_np.argsort.return_value = np.array([0, 2, 1])  # Sort by area (descending)
        
        # Call the function
        result = merge_faces(faces_list)
        
        # Two faces should be kept (face1 and face2) as face3 overlaps with face1
        self.assertEqual(len(result), 2)
        
        # Empty list should return empty array
        empty_result = merge_faces([])
        self.assertEqual(len(empty_result), 0)

if __name__ == '__main__':
    unittest.main()
