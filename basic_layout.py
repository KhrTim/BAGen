import gradio as gr
from utils.song_generator import generate_songs
from utils.generate_backgrounds import generate_backgrounds
from PIL import Image
import os
from utils.create_animation import create_cinemo_visualisation
from utils.style_transfer import perform_styleid_styletransfer
from utils.image_video_overlay_blend import overlay_effect_video
from utils.image_gif_overlay import overlay_image_with_gif


def song_generator_stub(phrase, num_of_samples):
    results = [
        [
            "**Song Title:** Whiskers & Whistle",
            "",
            "**Verse 1:**  ",
            "Whiskers the cat, so sly and bold,  ",
            "With eyes like fire, red devil cat, he's told.  ",
            "Tails swishin', paws on the ground,  ",
            "Chasing dreams, in the meadow bound.",
            "",
            "**Chorus:**  ",
            "Whiskers & Whistle, dancing under skies so wide,  ",
            "Red devil cat, with mischief in",
        ],
        [
            "**Verse 1:**",
            "In the meadow where daisies dance,  ",
            "Lives a **Red devil cat**, a sight to chance.  ",
            "With fur like fire, eyes aglow bright,  ",
            "She leaps through fields, a magical sight.",
            "",
            "**Chorus:**",
            "Oh, **Red devil cat**, oh so free,  ",
            "Fly high, let your spirit soar through the sky.  ",
            "Red devil cat, our friend so bold,  ",
            "In",
        ],
        [
            "**Title:** Red Devil's Dance",
            "",
            "**Verse 1:**  ",
            "In the garden where dreams begin,  ",
            "A red devil cat with paws so fine,  ",
            "Leaps through flowers, wild and free,  ",
            "Whispers secrets, leaves them to see.",
            "",
            "**Chorus:**  ",
            "Red devil cat, oh so sly,  ",
            "Dances in the moonlight, oh so bright!  ",
            "Fly high, sky's your limit,  ",
            "Red",
        ],
        [
            "**Verse 1:**",
            "In the meadow where the sun doth play,",
            "There lives a Red Devil Cat, so sly.",
            "With whiskers so soft and eyes so bright,",
            "He dances with the bees, under the light.",
            "",
            "**Chorus:**",
            "Oh, Red Devil Cat, oh, oh, oh!",
            "Bringing joy with each playful hop.",
            "Through meadows green and skies so blue,",
            "You're the delight, the shining cue.",
            "",
            "**Verse ",
        ],
        [
            "**Title:** Red Whiskers Whirl",
            "",
            "**Verse 1:**  ",
            "In the meadow where the daisies sway,  ",
            "A red devil cat with a mischievous play,  ",
            "Whiskers twitch, paws dance in the breeze,",
            "Chasing butterflies, no need to please.",
            "",
            "**Chorus:**  ",
            "Red whiskers whirl around, oh so bright,  ",
            "Dancing in the light, shining so right,  ",
            "Red devil cat,",
        ],
        [
            "**Title:** Whiskered Whizzer",
            "",
            "**Verse 1:**  ",
            "In the garden where flowers bloom,  ",
            "Lives a Red Devil Cat, she zooms around,  ",
            "Whiskers twitching, paws on the ground,  ",
            "Red Devil Cat dances, wild and unbound!",
            "",
            "**Chorus:**  ",
            "Oh, Red Devil Cat, whiskered whirlwind,  ",
            "Fly high, oh so swift, a whiskered whizz!  ",
            "Red",
        ],
    ]
    return results[:num_of_samples]


def generate_backgrounds_stub(lyrics, num):
    PATH_TO_IMAGE = "media/cat_img.webp"
    images = []
    for i in range(num):
        images.append(Image.open(PATH_TO_IMAGE))
    return images


with gr.Blocks() as demo:
    gr.Markdown("# NurseVRGen: Gekjfwjekf")
    contents_chosen = gr.State("")
    chosen_background = gr.State()
    style_transfer_image_path = gr.State()
    animation_video_path = gr.State("")
    final_video_path = gr.State("")

    with gr.Row():
        initial_phrase = gr.Textbox(label="Initial phrase for lyrics generation")
        number_of_samples = gr.Number(
            label="Number of samples", maximum=6, minimum=1, step=1, value=1
        )
        generate_button = gr.Button(value="Generate")

    @gr.render(
        inputs=[initial_phrase, number_of_samples], triggers=[generate_button.click]
    )
    def display_generated_lyrics(phrase, num_of_samples):
        # contents = [f"Some phrase {i} {phrase}" for i in range(num_of_samples)]
        raw_contents = song_generator_stub(phrase, num_of_samples)
        print(raw_contents)
        contents = []
        for lyrics in raw_contents:
            res = ""
            for token in lyrics:
                res += token + "\n"
            contents.append(res)

        print(contents)

        def selected_lyrics(sample, contents_chosen):
            print(contents_chosen)
            print(sample)
            return sample

            # gr.Textbox(value=contents[number])

        with gr.Row():
            for i in range(num_of_samples):
                with gr.Column():
                    lyrics_sample = gr.Textbox(value=contents[i])
                    select_button = gr.Button(value="Select")
                    select_button.click(
                        selected_lyrics,
                        inputs=[lyrics_sample, contents_chosen],
                        outputs=contents_chosen,
                    )

    @gr.render(inputs=contents_chosen, triggers=[contents_chosen.change])
    def display_images(cont):
        backgrounds = generate_backgrounds_stub(cont, 3)

        def selected_lyrics(sample, contents_chosen):
            print(contents_chosen)
            print(sample)
            return sample

        print("Function call: ", cont)
        with gr.Row(visible=True):
            for i in range(len(backgrounds)):
                with gr.Column():
                    image_sample = gr.Image(backgrounds[i], type="pil")
                    select_button = gr.Button(value="Select")
                    select_button.click(
                        selected_lyrics,
                        inputs=[image_sample, chosen_background],
                        outputs=chosen_background,
                    )

    @gr.render(triggers=[chosen_background.change])
    def input_animation_options():
        def create_animation(params):
            print("=============================")
            if params[style_transfer_image_path]:
                print("Image exists")
            else:
                print("Image doesn't exits")
                print("preset: ")
                print(params[preset])
                print("chosen_background")
                print(params[chosen_background])
                params[style_transfer_image_path] = perform_styleid_styletransfer(
                    params[preset], params[chosen_background]
                )
                print("PATH")
                print(params[style_transfer_image_path])

            params[animation_video_path] = create_cinemo_visualisation(
                params[prompt],
                Image.open(params[style_transfer_image_path]),
                params[intensity],
                params[num_frames],
            )

            print(params[prompt])
            print(params[animation_video_path])
            print(params[style_transfer_image_path])

            return (
                params[style_transfer_image_path],
                params[animation_video_path],
                gr.Row(visible=True),
                gr.Video(params[animation_video_path], visible=True),
            )

        def manage_animation_behavior_input_row(option):
            if option == 0:
                return gr.Row(visible=True), gr.Video(), gr.Row(visible=False), gr.Row()
            elif option == 1:
                return (
                    gr.Row(visible=False),
                    gr.Video(visible=False),
                    gr.Row(visible=True),
                    gr.Row(visible=False),
                )

        def overlay_background_with_animation(params):
            path_to_file = os.path.join("media", "result")
            OVERLAY_VIDEO_SAVE_PATH = os.path.join(path_to_file, "final.mp4")
            if not os.path.exists(path_to_file):
                os.makedirs(path_to_file, exist_ok=True)

            overlay_effect_video(
                params[animation_video_path],
                params[chosen_background],
                OVERLAY_VIDEO_SAVE_PATH,
                params[alpha],
            )
            params[final_video_path] = OVERLAY_VIDEO_SAVE_PATH
            return params[final_video_path], gr.Video(params[final_video_path])

        def overlay_background_with_gif(params):
            path_to_file = os.path.join("media", "result")
            OVERLAY_GIF_SAVE_PATH = os.path.join(path_to_file, "final.gif")
            if not os.path.exists(path_to_file):
                os.makedirs(path_to_file, exist_ok=True)

            print("GIF CREATED")

            # overlay_image_with_gif(background: PIL.Image.Image, gif: PIL.Image.Image, opacity: float, output_filename: os.PathLike):
            overlay_image_with_gif(
                params[chosen_background],
                params[preset],
                params[gif_alpha],
                OVERLAY_GIF_SAVE_PATH,
            )
            # params[final_video_path] = OVERLAY_GIF_SAVE_PATH
            # return params[final_video_path], gr.Video(params[final_video_path])

            return OVERLAY_GIF_SAVE_PATH

        effect_option = gr.Radio(
            ["Generate effect from static image asset", "Overlay GIF"],
            label="Effect",
            type="index",
        )

        with gr.Row():
            preset = gr.Image(type="pil", height=500)
            animation_effect_preview = gr.Video(visible=False)

        with gr.Row(visible=False) as animation_behavior:
            prompt = gr.Textbox(label="Description of a desired animation behavior")
            intensity = gr.Slider(
                minimum=1,
                maximum=19,
                step=1,
                value=10,
                label="Animation intensity",
                interactive=True,
            )
            num_frames = gr.Slider(
                minimum=1,
                maximum=50,
                step=1,
                value=10,
                label="Number of animation steps",
                interactive=True,
            )
            create_button = gr.Button(value="Create")

        with gr.Row(visible=False) as gif_final_step:
            with gr.Column():
                gif_alpha = gr.Slider(
                    maximum=1, value=0.5, step=0.1, minimum=0.2, interactive=True
                )
                gif_final_animation = gr.Image(show_download_button=True, height=800)
                gif_alpha.change(
                    overlay_background_with_gif,
                    inputs={gif_alpha, preset, chosen_background},
                    outputs=gif_final_animation,
                )

        with gr.Row(visible=False) as video_final_step:
            with gr.Column():
                alpha = gr.Slider(maximum=1, value=0.5, step=0.1, interactive=True)
                final_animation = gr.Video(
                    show_download_button=True, autoplay=True, height=800
                )
                alpha.change(
                    overlay_background_with_animation,
                    inputs={
                        alpha,
                        animation_video_path,
                        chosen_background,
                        final_video_path,
                    },
                    outputs=[final_video_path, final_animation],
                )

        # def print_input(value):
        #     print(value)

        preset.input(
            overlay_background_with_gif,
            inputs={gif_alpha, preset, chosen_background},
            outputs=gif_final_animation,
        )

        effect_option.input(
            manage_animation_behavior_input_row,
            inputs=effect_option,
            outputs=[
                animation_behavior,
                animation_effect_preview,
                gif_final_step,
                video_final_step,
            ],
        )

        create_button.click(
            overlay_background_with_animation,
            inputs={alpha, animation_video_path, chosen_background, final_video_path},
            outputs=[final_video_path, final_animation],
        )
        create_button.click(
            create_animation,
            inputs={
                prompt,
                intensity,
                num_frames,
                style_transfer_image_path,
                preset,
                chosen_background,
                animation_video_path,
            },
            outputs=[
                style_transfer_image_path,
                animation_video_path,
                video_final_step,
                animation_effect_preview,
            ],
        )


if __name__ == "__main__":
    demo.launch()
