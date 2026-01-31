from ultralytics import YOLO
import cv2
import os
import config
from PIL import Image
import numpy as np

# Fix for PyTorch 2.6+ weights_only issue
# Disable strict weights checking for trusted YOLO models
os.environ['TORCH_FORCE_WEIGHTS_ONLY_LOAD'] = '0'

class FaceDetector:
    """YOLOv8-based face detection service"""

    def __init__(self):
        """Initialize the YOLO model"""
        model_path = os.path.join(config.MODEL_FOLDER, config.MODEL_NAME)

        # Load YOLOv8 model (will download if not present)
        # For face detection, we'll use the standard YOLO model
        # You can fine-tune it on face datasets for better results
        self.model = YOLO(config.MODEL_NAME)
        self.confidence_threshold = config.MODEL_CONFIDENCE

    def detect_faces_in_image(self, image_path, output_path):
        """
        Detect faces in a single image

        Args:
            image_path: Path to input image
            output_path: Path to save output image with detections

        Returns:
            dict: Detection results with face count and confidence scores
        """
        # Read image
        image = cv2.imread(image_path)

        # Run YOLO detection
        results = self.model(image, conf=self.confidence_threshold)

        # Process results
        face_count = 0
        detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                # YOLO detects 'person' class (0) - we'll use this for face detection
                # For dedicated face detection, you'd use a face-specific model
                if class_id == 0:  # Person class
                    face_count += 1
                    detections.append({
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'confidence': confidence
                    })

                    # Draw bounding box
                    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)),
                                (0, 255, 0), 2)

                    # Add confidence label
                    label = f'Face: {confidence:.2f}'
                    cv2.putText(image, label, (int(x1), int(y1) - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save output image
        cv2.imwrite(output_path, image)

        return {
            'face_count': face_count,
            'detections': detections,
            'output_path': output_path
        }

    def detect_faces_in_video(self, video_path, output_path):
        """
        Detect faces in a video file

        Args:
            video_path: Path to input video
            output_path: Path to save output video with detections

        Returns:
            dict: Detection results with total faces detected
        """
        # Open video
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        total_detections = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process every Nth frame for efficiency
            if frame_count % config.PROCESS_EVERY_N_FRAMES == 0:
                # Run detection
                results = self.model(frame, conf=self.confidence_threshold)

                # Draw detections
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])

                        if class_id == 0:  # Person class
                            total_detections += 1

                            # Draw bounding box
                            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                        (0, 255, 0), 2)

                            label = f'Face: {confidence:.2f}'
                            cv2.putText(frame, label, (int(x1), int(y1) - 10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Write frame to output
            out.write(frame)
            frame_count += 1

        # Release resources
        cap.release()
        out.release()

        return {
            'total_frames': total_frames,
            'processed_frames': frame_count,
            'total_detections': total_detections,
            'output_path': output_path
        }

    def detect_faces_in_frame(self, frame):
        """
        Detect faces in a single frame (for webcam streaming)

        Args:
            frame: OpenCV frame (numpy array)

        Returns:
            frame: Frame with drawn bounding boxes
        """
        # Run detection
        results = self.model(frame, conf=self.confidence_threshold)

        # Draw detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                if class_id == 0:  # Person class
                    # Draw bounding box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                (0, 255, 0), 2)

                    label = f'Face: {confidence:.2f}'
                    cv2.putText(frame, label, (int(x1), int(y1) - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

# Create a singleton instance
face_detector = FaceDetector()
