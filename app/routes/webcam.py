from flask import Blueprint, Response, render_template
import cv2
from app.services.face_detector import face_detector

webcam_bp = Blueprint('webcam', __name__)

# Global variable to store camera object
camera = None

def get_camera():
    """Get or create camera object"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return camera

def generate_frames():
    """
    Generate video frames with face detection for streaming

    Yields:
        bytes: JPEG encoded frame
    """
    camera = get_camera()

    while True:
        # Read frame from camera
        success, frame = camera.read()

        if not success:
            break

        # Detect faces in frame
        frame = face_detector.detect_faces_in_frame(frame)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)

        if not ret:
            continue

        # Convert to bytes
        frame_bytes = buffer.tobytes()

        # Yield frame in multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@webcam_bp.route('/webcam')
def webcam_page():
    """Render webcam page"""
    return render_template('index.html')

@webcam_bp.route('/video_feed')
def video_feed():
    """
    Video streaming route

    Returns:
        Response: Multipart stream of JPEG frames
    """
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@webcam_bp.route('/stop_webcam')
def stop_webcam():
    """Stop and release webcam"""
    global camera
    if camera is not None:
        camera.release()
        camera = None
    return {'status': 'stopped'}
