from PIL import Image, ImageSequence
import PIL
import os


def overlay_image_with_gif(
    background: PIL.Image.Image,
    gif: PIL.Image.Image,
    opacity: float,
    output_filename: os.PathLike,
):
    background = background.convert("RGBA")

    bg_width, bg_height = background.size
    gif_transparency = int(opacity * 255)

    frames = []

    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        frame = frame.resize((bg_width, bg_height), Image.LANCZOS)

        alpha_channel = frame.getchannel("A")
        alpha_channel = alpha_channel.point(lambda p: min(p, gif_transparency))

        frame.putalpha(alpha_channel)

        background_copy = background.copy()

        background_copy.paste(frame, (0, 0), frame)

        frames.append(background_copy)

    frames[0].save(
        output_filename,
        save_all=True,
        append_images=frames[1:],
        loop=0,  # Infinite loop
        duration=gif.info.get("duration", 100),  # Keep the original GIF frame duration
        disposal=2,  # Clear the frame before the next
    )
    return output_filename
