import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
import config

def allowed_file(filename):
    """
    Check if file extension is allowed

    Args:
        filename: Name of the file

    Returns:
        bool: True if extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def is_image(filename):
    """Check if file is an image"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_IMAGE_EXTENSIONS

def is_video(filename):
    """Check if file is a video"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_VIDEO_EXTENSIONS

def generate_unique_filename(original_filename):
    """
    Generate a unique filename using UUID and timestamp

    Args:
        original_filename: Original filename

    Returns:
        str: Unique filename with original extension
    """
    # Get file extension
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''

    # Generate unique name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    unique_filename = f"{timestamp}_{unique_id}.{ext}"

    return unique_filename

def save_uploaded_file(file, folder):
    """
    Save uploaded file with a unique filename

    Args:
        file: FileStorage object from Flask request
        folder: Destination folder

    Returns:
        str: Path to saved file or None if failed
    """
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = generate_unique_filename(secure_filename(file.filename))
        filepath = os.path.join(folder, filename)

        # Save file
        file.save(filepath)
        return filepath

    return None

def get_file_size(filepath):
    """
    Get file size in bytes

    Args:
        filepath: Path to file

    Returns:
        int: File size in bytes
    """
    return os.path.getsize(filepath)

def cleanup_old_files(folder, max_age_hours=24):
    """
    Clean up files older than specified hours

    Args:
        folder: Folder to clean
        max_age_hours: Maximum age in hours
    """
    current_time = datetime.now()

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)

        # Skip directories and .gitkeep
        if os.path.isdir(filepath) or filename == '.gitkeep':
            continue

        # Get file modification time
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))

        # Calculate age
        age_hours = (current_time - file_time).total_seconds() / 3600

        # Delete if too old
        if age_hours > max_age_hours:
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")
