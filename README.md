# Face Detection Web Application

A complete end-to-end deep learning application for facial detection using YOLOv8. This web application provides an intuitive interface for detecting faces in images, videos, and real-time webcam feeds.

## Features

- **Single Image Detection**: Upload and detect faces in individual images
- **Video Processing**: Process video files with frame-by-frame face detection
- **Batch Processing**: Upload and process multiple files simultaneously
- **Real-time Webcam**: Live face detection using your webcam
- **Clean UI**: Modern, responsive web interface
- **Download Results**: Save processed images and videos with bounding boxes

## Technology Stack

- **Backend**: Flask (Python web framework)
- **AI Model**: YOLOv8 (Ultralytics)
- **Computer Vision**: OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **Image Processing**: Pillow, NumPy

## Project Structure

```
facial-detection-app/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── routes/
│   │   ├── detection.py         # Detection endpoints
│   │   └── webcam.py            # Webcam streaming
│   ├── services/
│   │   └── face_detector.py     # YOLOv8 face detection logic
│   └── utils/
│       ├── file_handler.py      # File upload utilities
│       └── video_processor.py   # Video processing utilities
├── static/
│   ├── css/style.css            # Styling
│   ├── js/main.js               # Frontend logic
│   └── uploads/                 # Temporary uploads
├── templates/
│   ├── base.html                # Base template
│   ├── index.html               # Main interface
│   └── results.html             # Results display
├── models/                      # YOLO model weights
├── outputs/                     # Processed results
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore rules
└── run.py                       # Application entry point
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Webcam (optional, for real-time detection)

### Setup Steps

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### Single Image Detection

1. Click on the "Single Image" tab
2. Drag and drop an image or click "Choose Image"
3. Click "Detect Faces"
4. View results with bounding boxes around detected faces
5. Download the processed image

### Video Processing

1. Click on the "Video" tab
2. Upload a video file (MP4, AVI, MOV, etc.)
3. Click "Process Video"
4. Wait for processing (may take a few minutes depending on video length)
5. View and download the processed video

### Batch Upload

1. Click on the "Batch Upload" tab
2. Select multiple images or videos
3. Click "Process All Files"
4. View results for all processed files
5. Download individual results

### Real-time Webcam

1. Click on the "Webcam" tab
2. Click "Start Webcam"
3. Allow browser access to your webcam
4. See real-time face detection
5. Click "Stop Webcam" when done

## Configuration

Edit [config.py](config.py) to customize:

- **Upload Limits**: Maximum file sizes
- **Model Settings**: Confidence threshold, YOLO model version
- **Processing**: Frame skip rate for videos
- **File Types**: Allowed extensions

```python
# Example configuration
MODEL_CONFIDENCE = 0.5          # Detection confidence threshold
PROCESS_EVERY_N_FRAMES = 2      # Process every 2nd frame
MAX_IMAGE_SIZE = 16 * 1024 * 1024   # 16MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB
```

## Model Information

This application uses **YOLOv8** (You Only Look Once version 8) for face detection:

- **Model**: YOLOv8n (nano) - optimized for speed
- **Alternative**: Change to `yolov8m.pt` in [config.py](config.py) for better accuracy
- **Auto-download**: Model weights are automatically downloaded on first run
- **Location**: Stored in the `models/` folder

### Using a Custom Face Detection Model

For better face-specific detection, you can train YOLOv8 on face datasets like WIDER FACE:

1. Download a face-specific YOLOv8 model
2. Place it in the `models/` folder
3. Update `MODEL_NAME` in [config.py](config.py)

## API Endpoints

The application provides the following REST API endpoints:

- `GET /` - Main web interface
- `POST /detect/image` - Upload and detect faces in image
- `POST /detect/video` - Upload and process video
- `POST /detect/batch` - Batch process multiple files
- `GET /video_feed` - Webcam video stream
- `GET /outputs/<filename>` - Download processed files

## Troubleshooting

### Model Download Issues

If the YOLO model fails to download automatically:
1. Manually download YOLOv8n from [Ultralytics](https://github.com/ultralytics/assets/releases)
2. Place `yolov8n.pt` in the `models/` folder

### Webcam Not Working

- Ensure browser permissions allow webcam access
- Check that no other application is using the webcam
- Try a different browser (Chrome/Firefox recommended)

### Large Video Processing

- For long videos, processing may take several minutes
- Increase `PROCESS_EVERY_N_FRAMES` in [config.py](config.py) to speed up processing
- Consider splitting large videos into smaller segments

### Port Already in Use

If port 5000 is already in use:
1. Edit [run.py](run.py)
2. Change `app.run(debug=True, port=5000)` to a different port (e.g., `port=8000`)

## Performance Tips

1. **For faster processing**: Use YOLOv8n (nano model)
2. **For better accuracy**: Use YOLOv8m (medium model)
3. **For large videos**: Increase frame skip rate
4. **For production**: Set `debug=False` in [run.py](run.py)

## Development

### Adding New Features

The modular structure makes it easy to extend:

- Add routes in [app/routes/](app/routes/)
- Add services in [app/services/](app/services/)
- Add utilities in [app/utils/](app/utils/)
- Add templates in [templates/](templates/)

### Running in Production

For production deployment:

1. Set `debug=False` in [run.py](run.py)
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure environment variables for sensitive data
4. Set up proper logging
5. Use a reverse proxy (Nginx, Apache)

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## License

This project is open source and available for educational and commercial use.

## Credits

- **YOLOv8**: [Ultralytics](https://github.com/ultralytics/ultralytics)
- **OpenCV**: Computer vision library
- **Flask**: Python web framework

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Contact the development team

## Changelog

### Version 1.0.0 (2024)
- Initial release
- Single image detection
- Video processing
- Batch upload
- Real-time webcam detection
- Modern web interface

---

Built with YOLOv8 and Flask
