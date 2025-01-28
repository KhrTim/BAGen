import os
import subprocess

import PIL

from .common import copy_image_to_subdirectory, get_list_of_files

CINEMO_DIR = os.path.join("submodules","Cinemo")

def create_cinemo_visualisation(prompt:str, image_asset: PIL.Image, visualization_intensity: int, num_frames: int) -> os.PathLike:
    cinemo_asses_dir = os.path.join(CINEMO_DIR, "animated_images")
    filename = copy_image_to_subdirectory(image_asset, cinemo_asses_dir)
    print(filename)

    # subprocess.call(["python","pipelines/animation.py", "--image_name", "00.jpg", "--prompt", f"'{prompt}'",  "--intensity", str(visualization_intensity), "--frames", str(num_frames)], cwd="./submodules/Cinemo/")
 
    visualization_dir = os.path.join(CINEMO_DIR, "sample_videos")
    visualzation_filename = get_list_of_files(visualization_dir)[0]
    print(visualization_dir)
    print(visualzation_filename)

    return visualzation_filename