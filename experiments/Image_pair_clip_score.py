import PIL.Image
import torch
from transformers import CLIPImageProcessor, CLIPModel
import PIL

def calcualte_clip_cosine_similarity(image_a, image_b, clip_model):
    # Load the two images and preprocess them for CLI

    # Calculate the embeddings for the images using the CLIP model
    with torch.no_grad():
        embedding_a = clip_model.get_image_features(image_a)
        embedding_b = clip_model.get_image_features(image_b)

    # Calculate the cosine similarity between the embeddings
    similarity_score = torch.nn.functional.cosine_similarity(embedding_a, embedding_b)

    # Print the similarity score
    print('Similarity score:', similarity_score.item())


def image_pair_clip_score(image_a: PIL.Image, image_b: PIL.Image, model, clip_preprocessor):
    image_a = clip_preprocessor(image_a, return_tensors="pt")["pixel_values"]
    image_b = clip_preprocessor(image_b, return_tensors="pt")["pixel_values"]
    return image_pair_clip_score(image_a, image_b, model)



if __name__ == "__main__":
    model_ID = "openai/clip-vit-base-patch32"
    model = CLIPModel.from_pretrained(model_ID)
    clip_preprocessor = CLIPImageProcessor.from_pretrained(model_ID)
    image_a = PIL.Image.open('/content/bla.png')
    image_b = PIL.Image.open('/content/bla.png')

    image_pair_clip_score(image_a, image_b, model, clip_preprocessor)
