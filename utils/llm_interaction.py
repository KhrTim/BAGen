import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
import re

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_songs(key_phrase, num_songs):
    model_name = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
    )

    messages = [
        {
            "role": "system",
            "content": "You are EXAONE model from LG AI Research, a helpful assistant.",
        },
        {
            "role": "user",
            "content": f"Generate a very short song for children containing following key-phrase: {key_phrase}.",
        },
    ]
    input_ids = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=False, return_tensors="pt"
    )

    # Set generation parameters
    num_return_sequences = num_songs  # Number of different outputs
    max_length = 150  # Maximum length of the generated sequences
    top_k = 50  # Top-k sampling
    top_p = 0.95  # Top-p (nucleus) sampling
    temperature = 0.7  # Adjust the randomness of the output

    # Generate multiple sequences
    outputs = model.generate(
        input_ids.to("cuda"),
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        do_sample=True,  # Enable sampling
        top_k=top_k,  # Top-k sampling
        top_p=top_p,  # Top-p sampling
        temperature=temperature,  # Adjust randomness
        pad_token_id=tokenizer.eos_token_id,  # Avoid warnings about padding
    )

    results = []
    # Decode and display the generated sequences
    for _, output in enumerate(outputs):
        decoded = tokenizer.decode(output, skip_special_tokens=True).split("\n")
        results.append(decoded[3:])

    del model
    torch.cuda.empty_cache()

    return results


def generate_animation_prompt(lyrics):
    logging.info("GENERATION OF ANIMATION PROMPT")
    model_name = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
    )

    messages = [
        {
            "role": "system",
            "content": "You are EXAONE model from LG AI Research, a helpful assistant.",
        },
        {
            "role": "user",
            "content": f"Generate a one line prompt that can be passed to animation generation model based on the following lyrics to create the best interactive and immersive experience: '{lyrics}'.",
        },
    ]

    input_ids = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=False, return_tensors="pt"
    )

    output = model.generate(
        input_ids.to("cuda"),
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=128,
        do_sample=False,
    )

    del model
    torch.cuda.empty_cache()
    output = tokenizer.decode(output[0], skip_special_tokens=True).split("\n")[-1]

    logging.info(output)

    match = re.search(r".*Prompt.*\s*\"([^\"]*)\"", output)

    if match:
        logging.debug("Found")
        extracted_text = match.group(1)
        logging.debug(f"PROMPT: {extracted_text}")
        return extracted_text
    logging.debug(f"PROMPT: {output}")
    return output[0]


if __name__ == "__main__":
    res = generate_animation_prompt("""Raindrops fall, soft and light,  
                                        Cat under rain, purring right.  
                                        Warm spots find comfort in sight,  
                                        Safe from storm, dreaming so bright.""")
    logging.debug(res)
