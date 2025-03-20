import uvicorn
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
import json

app = FastAPI()

@app.post("/predict")
def predict_image(file: UploadFile = File(...)):
    image = Image.open(file.file).resize((224, 224))
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    processed_img = preprocess_input(img_array)

    # Load the pre-trained ResNet50 model
    model = ResNet50(weights='imagenet')

    predictions = model.predict(processed_img)
    decoded_predictions = decode_predictions(predictions, top=3)[0]

    results = []
    for imagenet_id, name, prob in decoded_predictions:
        results.append({"label": name, "probability": float(prob)})
    return results

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
