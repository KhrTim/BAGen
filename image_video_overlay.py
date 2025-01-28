import cv2
import numpy as np

def overlay_effect_video(video_path, background_image_path, output_path):
    # Load the background image
    background_image = cv2.imread(background_image_path)
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
        print("Resizing video to match the background dimensions...")
        resize_frame = True
    else:
        resize_frame = False

    # Define the codec and output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (background_w, background_h))

    while True:
        ret, frame = video.read()
        if not ret:
            break  # End of video

        # Resize frame to match background dimensions
        if resize_frame:
            frame = cv2.resize(frame, (background_w, background_h))


        # Define the green color range for masking
        # lower_green = np.array([80, 140, 80])  # Lower bound for green in RGB
        # upper_green = np.array([220, 255, 220])  # Upper bound for green in RGB
        lower_green = np.array([255, 255, 255])  # Lower bound for green in RGB
        upper_green = np.array([255, 255, 255])  # Upper bound for green in RGB
        
        mask = cv2.inRange(frame, lower_green, upper_green)

        # Invert the mask to keep non-green parts
        mask_inv = cv2.bitwise_not(mask)

        # Extract the non-green areas of the video
        foreground = cv2.bitwise_and(frame, frame, mask=mask_inv)

        # Extract the corresponding area of the background image
        background_part = cv2.bitwise_and(background_image, background_image, mask=mask)

        # Combine the two parts
        combined_frame = cv2.add(foreground, background_part)

        # Write the frame to the output video
        out.write(combined_frame)

        # Display for debugging (optional)
        cv2.imshow('Overlay Effect', combined_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    video.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved at: {output_path}")

# Example usage:
overlay_effect_video("raindrops_2.mp4", "11.jpg", "output_video_3.mp4")