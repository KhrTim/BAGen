import cv2
import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def overlay_effect_video(video_path, background_image, output_path, alpha: float = 0.5):
    background_image = cv2.cvtColor(np.array(background_image), cv2.COLOR_RGB2BGR)
    logging.info("Background image loaded")
    background_h, background_w, _ = background_image.shape

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        logging.info("Error: Could not open the video file.")
        return

    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if frame_width != background_w or frame_height != background_h:
        resize_frame = True
    else:
        resize_frame = False

    fourcc = cv2.VideoWriter_fourcc(*"VP09")
    out = cv2.VideoWriter(output_path, fourcc, fps, (background_w, background_h))

    while True:
        ret, frame = video.read()
        if not ret:
            break

        if resize_frame:
            frame = cv2.resize(frame, (background_w, background_h))

        blended_frame = cv2.addWeighted(frame, alpha, background_image, 1 - alpha, 0)

        out.write(blended_frame)

    video.release()
    out.release()
    cv2.destroyAllWindows()
    logging.info(f"Video saved at: {output_path}")
    return output_path


# Example usage:
# overlay_effect_video("stylized_raindrops.mp4", "11.jpg", "output_video_3.mp4")
