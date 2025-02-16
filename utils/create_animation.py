import os
import subprocess
import logging
import PIL
from .common import (
    copy_image_to_subdirectory,
    get_list_of_files,
    delete_files_in_directory,
)
import shutil
from .video_converter import convert_video

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

CINEMO_DIR = os.path.join("submodules", "Cinemo")


def create_cinemo_visualisation(
    prompt: str,
    image_asset: PIL.Image,
    visualization_intensity: int,
    num_animation_steps: int,
    video_len_frames: int,
    save_path: os.PathLike,
) -> os.PathLike:
    logging.debug("++++++++ ASSET ++++++++")
    logging.debug(image_asset)
    cinemo_asses_dir = os.path.join(CINEMO_DIR, "animated_images")
    delete_files_in_directory(cinemo_asses_dir)
    filename = copy_image_to_subdirectory(image_asset, cinemo_asses_dir)
    logging.debug(filename)
    visualization_dir = os.path.join(CINEMO_DIR, "sample_videos")
    delete_files_in_directory(visualization_dir)

    subprocess.run(
        [
            "python",
            "pipelines/animation.py",
            "--image_name",
            "00.jpg",
            "--prompt",
            f"'{prompt}'",
            "--intensity",
            str(visualization_intensity),
            "--num_sampling_steps",
            str(num_animation_steps),
            "--video_length",
            str(video_len_frames),
        ],
        cwd="./submodules/Cinemo/",
    )

    logging.debug("Subprocess fininsh")

    visualzation_filename = get_list_of_files(visualization_dir)[0]
    convert_video(visualzation_filename, save_path)
    shutil.copy(visualzation_filename, save_path.removesuffix(".webm")+".mp4")
    logging.info(f"File saved as {visualzation_filename}")
    logging.info(f"File copied to {save_path}")

    logging.debug(visualization_dir)
    logging.debug(visualzation_filename)

    return save_path
