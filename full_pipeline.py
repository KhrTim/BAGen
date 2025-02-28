import argparse
import logging

from utils.llm_interaction import generate_songs, generate_animation_prompt, choose_effect_category
from utils.generate_backgrounds import generate_single_background
import os
from utils.create_animation import create_cinemo_visualisation
from utils.image_gif_overlay import overlay_image_with_gif
from utils.gif_picker import pick_random_file
from PIL import Image
from datetime import datetime

def generate_filename(prefix="res", ext="gif"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}.{ext}", f"{timestamp}.txt"


MEDIA_PATH = "media"
GIF_ASSETS_PATH = os.path.join(MEDIA_PATH, "gif_assets")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def prepare_prompt(lyrics_sample):
    effect_suggestion = generate_animation_prompt(lyrics_sample)
    logging.info("________PROMPT SUGGESTION________")
    logging.info(effect_suggestion)
    effect_category = choose_effect_category(effect_suggestion)
    logging.info("________EFFECT CATEGORY________")
    logging.info(effect_category)
    gif_effect_path = pick_random_file(os.path.join(GIF_ASSETS_PATH, effect_category))
    logging.info("________EFFECT PATH________")
    logging.info(gif_effect_path)

    return effect_suggestion, gif_effect_path

def create_animation(prompt, background, intensity, num_animation_steps, video_len_frames, filename):
    path_to_file = os.path.join("media", "result")
    ANIMATION_SAVE_PATH = os.path.join(path_to_file, filename)
    if not os.path.exists(path_to_file):
        os.makedirs(path_to_file, exist_ok=True)
    animation_video_path = create_cinemo_visualisation(
        prompt,
        background,
        intensity,
        num_animation_steps,
        video_len_frames,
        ANIMATION_SAVE_PATH
    )

    logging.debug(animation_video_path)

    return animation_video_path

def overlay_background_with_gif(preset, background, gif_alpha, filename):
    if not preset:
        return  
    path_to_file = os.path.join("media", "result")
    OVERLAY_GIF_SAVE_PATH = os.path.join(path_to_file, filename)
    if not os.path.exists(path_to_file):
        os.makedirs(path_to_file, exist_ok=True)

    overlay_image_with_gif(
        background,
        Image.open(preset),
        gif_alpha,
        OVERLAY_GIF_SAVE_PATH,
    )

    return OVERLAY_GIF_SAVE_PATH



def run_pipeline(prompt, mode):
    raw_contents = generate_songs(prompt, 1)
    logging.debug(raw_contents)
    contents = []
    for lyrics in raw_contents:
        res = ""
        for token in lyrics:
            res += token + "\n"
        contents.append(res)
    
    logging.info("____________Lyrics___________")
    logging.info(contents[0])
    effect_suggestion, gif_effect_path = prepare_prompt(contents[0])
    background = generate_single_background(contents[0])


    prompts_path = os.path.join("media", "prompts")
    if not os.path.exists(prompts_path):
        os.makedirs(prompts_path, exist_ok=True)

    if mode == "gif":
        res_filename, prompt_filename = generate_filename()
        result = overlay_background_with_gif(gif_effect_path, background, 0.5, res_filename)
    else:
        res_filename, prompt_filename = generate_filename(ext="webm")
        result = create_animation(effect_suggestion, background, 15, 10, 15)
    
    with open(os.path.join(prompts_path, prompt_filename), "w") as out:
        out.write(contents[0])


    return result
    


def main():
    parser = argparse.ArgumentParser(description="Choose between 'gif' or 'direct animation'.")
    parser.add_argument("mode", choices=["gif", "direct"], help="Select the mode of operation.")
    parser.add_argument("prompt", help="Initial phrase that defines content to be created.")



    args = parser.parse_args()
    logging.info(f"Args: {args}")
    res = run_pipeline(args.prompt, args.mode)
    print(f"Result is saved at {res}")

if __name__ == "__main__":
    main()