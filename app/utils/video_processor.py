import cv2
import os
import numpy as np

def get_video_info(video_path):
    """
    Get video metadata

    Args:
        video_path: Path to video file

    Returns:
        dict: Video information (fps, width, height, frame_count)
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return None

    info = {
        'fps': int(cap.get(cv2.CAP_PROP_FPS)),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    }

    cap.release()
    return info

def extract_frames(video_path, output_folder, every_n_frames=10):
    """
    Extract frames from video

    Args:
        video_path: Path to video file
        output_folder: Folder to save frames
        every_n_frames: Extract every Nth frame

    Returns:
        list: Paths to extracted frames
    """
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frame_paths = []
    frame_count = 0
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save every Nth frame
        if frame_count % every_n_frames == 0:
            frame_path = os.path.join(output_folder, f'frame_{saved_count:04d}.jpg')
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            saved_count += 1

        frame_count += 1

    cap.release()
    return frame_paths

def create_video_from_frames(frame_paths, output_path, fps=30):
    """
    Create video from list of frame images

    Args:
        frame_paths: List of paths to frame images
        output_path: Path to output video
        fps: Frames per second

    Returns:
        str: Path to created video
    """
    if not frame_paths:
        return None

    # Read first frame to get dimensions
    first_frame = cv2.imread(frame_paths[0])
    height, width, _ = first_frame.shape

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Write all frames
    for frame_path in frame_paths:
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()
    return output_path

def estimate_processing_time(video_path, processing_speed=30):
    """
    Estimate video processing time

    Args:
        video_path: Path to video
        processing_speed: Frames per second processing speed

    Returns:
        float: Estimated time in seconds
    """
    info = get_video_info(video_path)
    if not info:
        return 0

    total_frames = info['frame_count']
    estimated_seconds = total_frames / processing_speed

    return estimated_seconds
