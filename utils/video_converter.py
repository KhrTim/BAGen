import cv2

def convert_video(input_file, output_file, fps=8):
    cap = cv2.VideoCapture(input_file)
    fourcc = cv2.VideoWriter_fourcc(*'VP09')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    print(f"Conversion completed: {output_file}")

if __name__ == "__main__":
    convert_video("/userHome/userhome1/timur/Projects/Nursery-Visual-Representation/submodules/Cinemo/sample_videos/final_result_0000_0000-imageio.mp4", "/userHome/userhome1/timur/Projects/Nursery-Visual-Representation/media/result/final.webm")