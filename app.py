from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
import shutil
import os
from PIL import Image
import io
from utils import *
from model_utils import *

app = FastAPI()
model, processor = setup_model()

UPLOAD_FOLDER = "uploaded_images"
OUTPUT_FOLDER = "output_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.post("/question-detect/")
async def question_detect(file: UploadFile = File(...)):
    try:
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        input_image = Image.open(image_path)
        doctags = process_input_image(input_image, processor, model, )
        parsed = parse_lines(doctags)
        q_lines = find_question_lines(parsed)
        
        question_crops = crop_questions(input_image, q_lines)
        return_img = concatenate_imgs(question_crops)    
        
        img_bytes = io.BytesIO()
        return_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        return Response(content=img_bytes.getvalue(), media_type="image/png")
    except:
        return Response(content=None)

@app.get("/")
def home():
    return {"message": "FastAPI Question Detection API"}
