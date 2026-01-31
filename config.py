import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
MODEL_FOLDER = os.path.join(BASE_DIR, 'models')

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv'}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS

# File size limits (in bytes)
MAX_IMAGE_SIZE = 16 * 1024 * 1024  # 16MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB

# YOLO model configuration
MODEL_CONFIDENCE = 0.5  # Confidence threshold for detection
MODEL_NAME = 'yolov8n.pt'  # YOLOv8 nano for speed (can use yolov8m.pt for better accuracy)

# Video processing
PROCESS_EVERY_N_FRAMES = 2  # Process every 2nd frame for efficiency

# Flask configuration
SECRET_KEY = 'your-secret-key-change-in-production'
MAX_CONTENT_LENGTH = MAX_VIDEO_SIZE

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)
