import gradio as gr
from song_generator import generate_songs
from generate_backgrounds import generate_backgrounds
from PIL import Image

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
    PATH_TO_IMAGE = "C:\\Users\\AutoML\\Documents\\LAB\\Automl_works\\Other_works\\children_song_paper\\app\\cat_img.webp"
    images = []
    for i in range(num):
        images.append(Image.open(PATH_TO_IMAGE))
    return images


with gr.Blocks() as demo:
    contents_chosen = gr.State("")
    chosen_background = gr.State()
    style_transfer_image_path = gr.State()


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
                    image_sample = gr.Image(backgrounds[i])
                    select_button = gr.Button(value="Select")
                    select_button.click(
                        selected_lyrics,
                        inputs=[image_sample, chosen_background],
                        outputs=chosen_background,
                    )
    


    @gr.render(triggers=[chosen_background.change])
    def display_images():

        def print_input(value):
            print(value)

        def manage_animation_behavior_input_row(option):
            if option == 0:
                return gr.Row(visible=True)
            elif option == 1:
                return gr.Row(visible=False)
        


        effect_option = gr.Radio(["Generate effect from static image asset", "Overlay GIF"], label="Effect",type='index')
        preset = gr.Image(type="pil")
        preset.input(print_input, inputs=preset)
        with gr.Row(visible=False) as animation_behavior:
            option = gr.Textbox(label="Description of a desired animation behavior")
            intensity = gr.Slider(minimum=1, maximum=19, step=1, value=10, label="Animation intensity", interactive=True)
            num_frames = gr.Slider(minimum=1, maximum=50, step=1, value=10, label="Number of animation steps", interactive=True)
            create_button = gr.Button(value="Create")


        effect_option.input(manage_animation_behavior_input_row, inputs=effect_option, outputs=animation_behavior)



if __name__ == "__main__":
    demo.launch()
