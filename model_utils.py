import time 
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

def setup_model():
    if torch.cuda.is_available():
        DEVICE = "cuda" 
    else:
        DEVICE = "cpu"
    print(DEVICE)
    processor = AutoProcessor.from_pretrained("ds4sd/SmolDocling-256M-preview")
    model = AutoModelForVision2Seq.from_pretrained(
        "ds4sd/SmolDocling-256M-preview",
        torch_dtype=torch.float16,
    ).to(DEVICE)
    return model, processor

def process_input_image(image, processor, model):
    messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "Convert this page to docling."}
        ]
    },
    ]    
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image], return_tensors="pt")
    inputs = inputs.to(model.device)
    t1 = time.time()
    generated_ids = model.generate(**inputs, max_new_tokens=8192, num_beams=2)
    t2 = time.time()
    print(f" Generation time is { t2 -t1}")
    prompt_length = inputs.input_ids.shape[1]
    trimmed_generated_ids = generated_ids[:, prompt_length:]
    doctags = processor.batch_decode(
        trimmed_generated_ids,
        skip_special_tokens=False,
    )[0]
    print(doctags)
    return doctags