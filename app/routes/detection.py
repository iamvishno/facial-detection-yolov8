from flask import Blueprint, render_template, request, jsonify, send_from_directory
import os
from app.services.face_detector import face_detector
from app.utils.file_handler import save_uploaded_file, is_image, is_video, cleanup_old_files
import config

detection_bp = Blueprint('detection', __name__)

@detection_bp.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@detection_bp.route('/detect/image', methods=['POST'])
def detect_image():
    """
    Handle single image upload and face detection

    Returns:
        JSON response with detection results
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate file type
        if not is_image(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400

        # Save uploaded file
        input_path = save_uploaded_file(file, config.UPLOAD_FOLDER)

        if not input_path:
            return jsonify({'error': 'Failed to save file'}), 500

        # Generate output path
        filename = os.path.basename(input_path)
        output_path = os.path.join(config.OUTPUT_FOLDER, filename)

        # Detect faces
        results = face_detector.detect_faces_in_image(input_path, output_path)

        # Clean up old files
        cleanup_old_files(config.UPLOAD_FOLDER)
        cleanup_old_files(config.OUTPUT_FOLDER)

        return jsonify({
            'success': True,
            'face_count': results['face_count'],
            'detections': results['detections'],
            'output_filename': filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@detection_bp.route('/detect/video', methods=['POST'])
def detect_video():
    """
    Handle video upload and face detection

    Returns:
        JSON response with detection results
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate file type
        if not is_video(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload a video.'}), 400

        # Save uploaded file
        input_path = save_uploaded_file(file, config.UPLOAD_FOLDER)

        if not input_path:
            return jsonify({'error': 'Failed to save file'}), 500

        # Generate output path
        filename = os.path.basename(input_path)
        output_path = os.path.join(config.OUTPUT_FOLDER, filename)

        # Detect faces in video
        results = face_detector.detect_faces_in_video(input_path, output_path)

        # Clean up old files
        cleanup_old_files(config.UPLOAD_FOLDER)
        cleanup_old_files(config.OUTPUT_FOLDER)

        return jsonify({
            'success': True,
            'total_frames': results['total_frames'],
            'processed_frames': results['processed_frames'],
            'total_detections': results['total_detections'],
            'output_filename': filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@detection_bp.route('/detect/batch', methods=['POST'])
def detect_batch():
    """
    Handle batch file upload and face detection

    Returns:
        JSON response with detection results for all files
    """
    try:
        # Check if files are present
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400

        files = request.files.getlist('files[]')

        if not files or len(files) == 0:
            return jsonify({'error': 'No files selected'}), 400

        results = []

        for file in files:
            if file.filename == '':
                continue

            # Save uploaded file
            input_path = save_uploaded_file(file, config.UPLOAD_FOLDER)

            if not input_path:
                results.append({
                    'filename': file.filename,
                    'error': 'Failed to save file'
                })
                continue

            # Generate output path
            filename = os.path.basename(input_path)
            output_path = os.path.join(config.OUTPUT_FOLDER, filename)

            # Detect faces based on file type
            if is_image(file.filename):
                detection_results = face_detector.detect_faces_in_image(input_path, output_path)
                results.append({
                    'filename': file.filename,
                    'type': 'image',
                    'face_count': detection_results['face_count'],
                    'output_filename': filename
                })
            elif is_video(file.filename):
                detection_results = face_detector.detect_faces_in_video(input_path, output_path)
                results.append({
                    'filename': file.filename,
                    'type': 'video',
                    'total_detections': detection_results['total_detections'],
                    'output_filename': filename
                })

        # Clean up old files
        cleanup_old_files(config.UPLOAD_FOLDER)
        cleanup_old_files(config.OUTPUT_FOLDER)

        return jsonify({
            'success': True,
            'results': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@detection_bp.route('/outputs/<filename>')
def get_output(filename):
    """
    Serve processed output files

    Args:
        filename: Name of the output file

    Returns:
        File response
    """
    return send_from_directory(config.OUTPUT_FOLDER, filename)

@detection_bp.route('/results/<filename>')
def show_results(filename):
    """
    Show detection results page

    Args:
        filename: Name of the output file

    Returns:
        Rendered results template
    """
    return render_template('results.html', filename=filename)
