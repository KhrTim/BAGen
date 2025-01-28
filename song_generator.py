import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
import random


def generate_songs(key_phrase, num_songs):
    model_name = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto"
    )

    messages = [
        {"role": "system", 
        "content": "You are EXAONE model from LG AI Research, a helpful assistant."},
        {"role": "user", "content": f"Generate a very short song for children containing following key-phrase: {key_phrase}."}
    ]
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=False,
        return_tensors="pt"
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
        pad_token_id=tokenizer.eos_token_id  # Avoid warnings about padding
    )

    results = []
    # Decode and display the generated sequences
    for _, output in enumerate(outputs):
        decoded = tokenizer.decode(output, skip_special_tokens=True).split('\n')
        results.append(decoded[3:])

    del model
    torch.cuda.empty_cache()

    return results

if __name__ == "__main__":
    res = generate_songs("blue bird", 3)
    print(res)