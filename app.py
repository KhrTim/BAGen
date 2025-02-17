import gradio as gr
from utils.llm_interaction import generate_songs, generate_animation_prompt, choose_effect_category
from utils.generate_backgrounds import generate_backgrounds
import os
from utils.create_animation import create_cinemo_visualisation
from utils.image_gif_overlay import overlay_image_with_gif
import logging
from utils.gif_picker import pick_random_file

MEDIA_PATH = "media"
GIF_ASSETS_PATH = os.path.join(MEDIA_PATH, "gif_assets")

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# NurseVRGen: Generative AI-based System for Visual Representation of Children's Songs"
    )

    contents_chosen = gr.State("")
    chosen_background = gr.State()
    animation_video_path = gr.State("")
    final_video_path = gr.State("")
    effect_suggestion = ""
    gif_effect_path = ""

    with gr.Row():
        initial_phrase = gr.Textbox(label="Initial phrase for lyrics generation")
        number_of_samples = gr.Number(
            label="Number of samples", maximum=6, minimum=1, step=1, value=3
        )
        generate_button = gr.Button(value="Generate")

    @gr.render(
        inputs=[initial_phrase, number_of_samples], triggers=[generate_button.click]
    )
    def display_generated_lyrics(phrase, num_of_samples):
        raw_contents = generate_songs(phrase, num_of_samples)

        logging.debug(raw_contents)
        contents = []
        for lyrics in raw_contents:
            res = ""
            for token in lyrics:
                res += token + "\n"
            contents.append(res)

        logging.debug(contents)

        #TODO: refactor. Too much for one function. Rename
        def choose_lyrics_and_prepare_prompt(lyrics_sample):
            global effect_suggestion
            global gif_effect_path
        
            effect_suggestion = generate_animation_prompt(lyrics_sample)
            logging.debug("________PROMPT SUGGESTION________")
            logging.debug(effect_suggestion)
            effect_category = choose_effect_category(effect_suggestion)
            logging.debug("________EFFECT CATEGORY________")
            logging.debug(effect_category)
            gif_effect_path = pick_random_file(os.path.join(GIF_ASSETS_PATH, effect_category))
            logging.debug("________EFFECT PATH________")
            logging.debug(gif_effect_path)

            return lyrics_sample
    
        with gr.Row():
            for i in range(num_of_samples):
                with gr.Column():
                    lyrics_sample = gr.Textbox(
                        value=contents[i], label=f"Result {i + 1}"
                    )
                    select_button = gr.Button(value="Select")
                    select_button.click(
                        choose_lyrics_and_prepare_prompt,
                        inputs=lyrics_sample,
                        outputs=contents_chosen
                    )

    @gr.render(inputs=contents_chosen, triggers=[contents_chosen.change])
    def display_images(cont):
        backgrounds = generate_backgrounds(cont)


        gr.Markdown("# Generated Backgrounds")
        with gr.Row(visible=True):
            for i in range(len(backgrounds)):
                with gr.Column():
                    image_sample = gr.Image(
                        backgrounds[i],
                        type="pil",
                        label=f"Result {i + 1}",
                        show_download_button=True,
                        interactive=False,
                    )
                    select_button = gr.Button(value="Select")
                    select_button.click(
                        lambda x: x,
                        inputs=image_sample,
                        outputs=chosen_background,
                    )

    @gr.render(triggers=[chosen_background.change])
    def animation_step():
        def create_animation(params):
            path_to_file = os.path.join("media", "result")
            ANIMATION_SAVE_PATH = os.path.join(path_to_file, "final.webm")
            if not os.path.exists(path_to_file):
                os.makedirs(path_to_file, exist_ok=True)
            params[animation_video_path] = create_cinemo_visualisation(
                params[prompt],
                params[chosen_background],
                params[intensity],
                params[num_animation_steps],
                params[video_len_frames],
                ANIMATION_SAVE_PATH
            )

            print(params[animation_video_path])

            return (
                params[animation_video_path],
                gr.Row(visible=True),
                gr.Video(params[animation_video_path], visible=True),
            )

        def manage_animation_behavior_input_row(option):
            if option == 0:
                return (
                    gr.Row(visible=True),
                    gr.Column(visible=False),
                    gr.Column(),
                    gr.Image(visible=False)
                )
            elif option == 1:
                return (
                    gr.Row(visible=False),
                    gr.Column(visible=True),
                    gr.Column(visible=False),
                    gr.Image(visible=True)
                )

        def overlay_background_with_gif(params):
            if not params[preset]:
                return  
            path_to_file = os.path.join("media", "result")
            OVERLAY_GIF_SAVE_PATH = os.path.join(path_to_file, "final.gif")
            if not os.path.exists(path_to_file):
                os.makedirs(path_to_file, exist_ok=True)

            overlay_image_with_gif(
                params[chosen_background],
                params[preset],
                params[gif_alpha],
                OVERLAY_GIF_SAVE_PATH,
            )

            return OVERLAY_GIF_SAVE_PATH

        gr.Markdown("# Effect generation")
        effect_option = gr.Radio(
            ["Generate effect from static image asset", "Overlay GIF"],
            label="Effect generation option",
            type="index",
        )

        preset = gr.Image(type="pil", height=500, label="Image or GIF asset", visible=False, value=gif_effect_path)

        with gr.Row(visible=False) as animation_behavior:
            with gr.Column():
                prompt = gr.Textbox(label="Description of a desired animation behavior", value=effect_suggestion, interactive=True)
                intensity = gr.Slider(
                    minimum=1,
                    maximum=19,
                    step=1,
                    value=10,
                    label="Animation intensity",
                    interactive=True,
                )
            with gr.Column():
                num_animation_steps = gr.Slider(
                    minimum=1,
                    maximum=50,
                    step=1,
                    value=10,
                    label="Number of animation steps",
                    interactive=True,
                )
                video_len_frames = gr.Slider(
                    minimum=15,
                    maximum=50,
                    step=1,
                    value=15,
                    label="Number of frames",
                    interactive=True,
                )
            create_button = gr.Button(value="Create")

        with gr.Column(visible=False) as gif_final_step:
            gr.Markdown("# Final Result")
            gif_alpha = gr.Slider(
                maximum=1,
                value=0.5,
                step=0.1,
                minimum=0.2,
                interactive=True,
                label="Effect transparency",
            )
            gif_final_animation = gr.Image(
                show_download_button=True, height=800, label="Result preview"
            )
            gif_alpha.change(
                overlay_background_with_gif,
                inputs={gif_alpha, preset, chosen_background},
                outputs=gif_final_animation,
            )

        with gr.Column(visible=False) as video_final_step:
            gr.Markdown("# Final Result")
            final_animation = gr.Video(
                show_download_button=True,
                autoplay=True,
                height=800,
                label="Result preview",
            )

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
                gif_final_step,
                video_final_step,
                preset
            ],
        )

        create_button.click(
            create_animation,
            inputs={
                prompt,
                intensity,
                num_animation_steps,
                chosen_background,
                animation_video_path,
                video_len_frames
            },
            outputs=[
                animation_video_path,
                video_final_step,
                final_animation,
            ],
        )


if __name__ == "__main__":
    demo.launch(share=True)
