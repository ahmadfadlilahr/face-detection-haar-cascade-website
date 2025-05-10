# Face Detection with Haar Cascade

A real-time face detection application using OpenCV's Haar Cascade classifiers, with both desktop and web interfaces.

Copyright (c) 2025, [Ahmad Fadlilah](https://github.com/ahmadfadlilah)

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Active-brightgreen)](https://ahmadfadlilahr.github.io/face-detection-haar-cascade/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project implements a real-time face detection system using a webcam and Haar Cascade classifiers from OpenCV. The application detects faces in the video feed, draws rectangles around them, and displays the count of detected faces. Histogram equalization is applied to improve face detection in varying lighting conditions.

The project includes a web interface for a more user-friendly experience and a desktop application to help manage the web server!

## Features

- Real-time face detection from webcam
- Web interface for accessing the application through a browser
- Upload and process images through the web interface
- Face detection on uploaded images
- Automatic download of cascade files if not present
- Face count display
- Histogram equalization for improved detection in varying light conditions
- Graceful error handling and webcam initialization
- Desktop application to control web server

## Demo Website

Visit our [GitHub Pages Demo](https://ahmadfadlilahr.github.io/face-detection-haar-cascade/) to explore documentation and see the project in action.

## Quick Start

For Windows users:

1. Run `init-project.bat` to set up the environment and install dependencies
2. Run `start-desktop-app.bat` to launch the desktop application
3. Click "Start Web Server" and then "Open Browser"
4. Use the web interface to detect faces via webcam or upload images

For detailed instructions, see [Quick Start Guide](docs/quickstart.md).

## Requirements

- Python 3.6 or newer
- OpenCV
- NumPy
- Requests
- Flask (for web interface)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourahmadfadlilahr/face-detection-haar-cascade.git
cd face-detection-haar-cascade
```

2. Initialize the project:
```
init-project.bat
```

Or install dependencies manually:
```
pip install -r requirements.txt
```

## Usage

### Web Interface

To run the application with web interface:

```
python src/app.py
```

Or simply run:
```
start-web-app.bat
```

Then open your browser and navigate to:
```
http://localhost:5000
```

### Desktop Launcher

To run the desktop application launcher:

```
python src/desktop_app.py
```

### Command Line

To run the original face detection application from command line:

```
python src/face_detection.py
```

### Jupyter Notebook

Or open and run the Jupyter notebook:

```
jupyter notebook deteksi_lokal.ipynb
```

Press 'q' to exit the command-line application while it's running.

## Project Structure

```
├── LICENSE
├── README.md
├── requirements.txt
├── src/
│   ├── app.py               # Web application
│   ├── desktop_app.py       # Desktop launcher for web app
│   ├── face_detection.py    # Core face detection module
│   └── templates/           # Web templates
│       └── index.html       # Main web interface
└── deteksi_lokal.ipynb      # Jupyter notebook implementation
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV team for providing the Haar Cascade classifiers
- Computer vision community for tutorials and resources
