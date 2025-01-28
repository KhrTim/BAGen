import PIL
import PIL.Image
import os
from transparent_background import Remover
import subprocess
from rembg import remove



CINEMO_DIR = "submodules/Cinemo"
STYLEID_DIR = "submodules/StyleID"

def delete_files_in_directory(directory_path):
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def get_list_of_files(directory_path):
    files = []
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files

def cleanup(directories_to_cleanup: list[os.PathLike]):
    for directory in directories_to_cleanup:
        delete_files_in_directory(directory)


def copy_image_to_subdirectory(image_asset: PIL.Image, subdirectory):
    filename = os.path.join(subdirectory,"00.jpg")
    print(filename)
    # image_asset.convert('RGB')
    image_asset.save(filename)
    return filename

# def change_config_file(config_filename, , visualization_intensity: int, num_frames: int)


def create_cinemo_visualisation(prompt:str, image_asset: PIL.Image, visualization_intensity: int, num_frames: int):
    cinemo_asses_dir = os.path.join(CINEMO_DIR, "animated_images")
    filename = copy_image_to_subdirectory(image_asset, cinemo_asses_dir)
    print(filename)

    subprocess.call(["python","pipelines/animation.py", "--image_name", "00.jpg", "--prompt", f"'{prompt}'",  "--intensity", str(visualization_intensity), "--frames", str(num_frames)], cwd="./submodules/Cinemo/")
    # subprocess.call(["python","pipelines/animation.py", f"--image_name '00.jpg' --prompt '{prompt}' --intensity {visualization_intensity} --frames {num_frames}"], cwd="./submodules/Cinemo/")


    visualization_dir = os.path.join(CINEMO_DIR, "animated_images")
    visualzation_filename = get_list_of_files(visualization_dir)[0]
    print(visualization_dir)
    print(visualzation_filename)

    return visualzation_filename


def remove_background(input_image: os.PathLike):

    input = PIL.Image.open(input_image)
    output = remove(input)
    return output.convert("RGB")


    # remover = Remover(device='cuda:0')
    # img = PIL.Image.open(input_image).convert('RGB')
    
    # return remover.process(img, type='green')


def perform_styleid_styletransfer(content_image: PIL.Image, style_image: PIL.Image):
    style_id_content_dir = os.path.join(STYLEID_DIR, "data", "cnt")
    style_id_style_dir = os.path.join(STYLEID_DIR, "data", "sty")

    copy_image_to_subdirectory(content_image, style_id_content_dir)
    copy_image_to_subdirectory(style_image, style_id_style_dir)
    
    subprocess.call(["python","run_styleid.py"], cwd="./submodules/StyleID/")

    visualization_dir = os.path.join(STYLEID_DIR, "output")
    style_transfer_image_filename = get_list_of_files(visualization_dir)[0]

    # print(style_transfer_image_filename)

    # background_removed = remove_background(style_transfer_image_filename)

    # print(background_removed)
    # background_removed.save("Background_removed.jpg")
    return PIL.Image.open(style_transfer_image_filename)

if __name__ == "__main__":
    # perform_styleid_styletransfer(PIL.Image.open("rain.png").convert('RGB'), PIL.Image.open("cat.webp").convert('RGB'))
    # create_cinemo_visualisation("Rain drops fall down", PIL.Image.open("rain.png").convert('RGB'), 10, 10)

    create_cinemo_visualisation("Rain drops fall down", PIL.Image.open("00_stylized_00.png").convert('RGB'), 10, 10)



