from PIL import Image
import os
from datetime import datetime
import cv2


def gif_to_frames(path_to_gif):
    frames_path = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(frames_path):
        os.makedirs(frames_path, exist_ok=True)


    gif = Image.open(path_to_gif)

    frame_count = 0
    while True:
        frame_filename = os.path.join(frames_path, f"frame_{frame_count:06d}.png")
        gif.save(frame_filename)  # Save the current frame as an image
        
        frame_count += 1
        try:
            gif.seek(frame_count)  # Move to next frame
        except EOFError:
            break  # Stop when no more frames are left

if __name__ == "__main__":
    g_path = "experiments/final.gif"
    gif_to_frames(g_path)


