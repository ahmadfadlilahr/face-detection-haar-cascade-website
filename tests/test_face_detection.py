#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for face detection functionality
Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)
"""

import os
import sys
import unittest
from unittest.mock import patch

# Add the src directory to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestFaceDetection(unittest.TestCase):
    """Test cases for face detection functionality"""
    
    def test_imports(self):
        """Test that required libraries can be imported"""
        try:
            import cv2
            import numpy as np
            import requests
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import error: {e}")
    
    @patch('cv2.CascadeClassifier')
    def test_cascade_classifier_creation(self, mock_classifier):
        """Test that cascade classifier can be created"""
        # Mock the return value of CascadeClassifier
        mock_classifier.return_value.empty.return_value = False
        
        from src.face_detection import cv2
        
        # Creating a cascade classifier should not raise exceptions
        classifier = cv2.CascadeClassifier('dummy_path')
        self.assertFalse(classifier.empty())

if __name__ == '__main__':
    unittest.main()
