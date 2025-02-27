import os
from datetime import datetime
import cv2


def video_to_frames(path_to_video):
    frames_path = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(frames_path):
        os.makedirs(frames_path, exist_ok=True)

    cap = cv2.VideoCapture(path_to_video)

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Stop if the video ends
        
        # Save frame as an image
        frame_filename = os.path.join(frames_path, f'frame_{frame_count:06d}.jpg')
        cv2.imwrite(frame_filename, frame)
        
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    v_path = "experiments/final.mp4"
    video_to_frames(v_path)
