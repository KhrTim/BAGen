import cv2
import numpy as np


def overlay_effect_video(video_path, background_image, output_path, alpha: float = 0.5):
    # Load the background image
    # background_image = cv2.imread(background_image_path)
    # background_image = cv2.imread(background_image_path)
    background_image = cv2.cvtColor(np.array(background_image), cv2.COLOR_RGB2BGR)
    print("Background image loaded")
    background_h, background_w, _ = background_image.shape

    # Open the video file
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Error: Could not open the video file.")
        return

    # Get video properties
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Resize the video frame to match the background if needed
    if frame_width != background_w or frame_height != background_h:
        resize_frame = True
    else:
        resize_frame = False

    # Define the codec and output video
    fourcc = cv2.VideoWriter_fourcc(*"h264")
    out = cv2.VideoWriter(output_path, fourcc, fps, (background_w, background_h))

    while True:
        ret, frame = video.read()
        if not ret:
            break  # End of video

        # Resize frame to match background dimensions
        if resize_frame:
            frame = cv2.resize(frame, (background_w, background_h))

        blended_frame = cv2.addWeighted(frame, alpha, background_image, 1 - alpha, 0)

        # Write the frame to the output video
        out.write(blended_frame)

    # Release resources
    video.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved at: {output_path}")
    return output_path


# Example usage:
# overlay_effect_video("stylized_raindrops.mp4", "11.jpg", "output_video_3.mp4")
