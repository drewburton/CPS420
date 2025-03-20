import base64
import io
import ssl
from typing import List
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
import json
import matplotlib.pyplot as plt

app = FastAPI()
ssl._create_default_https_context = ssl._create_unverified_context

class PredictionResult(BaseModel): 
    filename: str 
    predictions: List[dict]
    
def generate_plot(data: PredictionResult):
    labels = [item["label"] for item in data.predictions]
    probabilities = [item["probability"] for item in data.predictions]
    # 1. Generate the image in memory (Matplotlib example)
    fig, ax = plt.subplots()
    ax.bar(labels, probabilities)
    plt.xlabel("Labels")
    plt.ylabel("Probability")
    plt.ylim(0, max(probabilities) * 1.1) #Sets the y limit a little above the max value.
    for i, prob in enumerate(probabilities):
        #Add probability values above each bar.
        ax.text(i, prob + 0.002, f'{prob:.4f}', ha='center', va='bottom')

    # 2. Encode the image to base64
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    plt.close(fig) #Important to close the figure.
    return img_base64

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    try:
        print("in endpoint")
        image = Image.open(file.file).convert("RGB").resize((224, 224))
        img_array = np.array(image)
        img_array = np.expand_dims(img_array, axis=0)
        processed_img = preprocess_input(img_array)
        print("processed image")
        model = ResNet50(weights='imagenet')
        predictions = model.predict(processed_img)
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        print("made predictions")
        results = []
        for imagenet_id, name, prob in decoded_predictions:
            results.append({"label": name, "probability": float(prob)})
        print("generating plot")
        img_base64 = generate_plot(PredictionResult(filename=file.filename, predictions=results))
        print("generated plot")
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Result</title>
        </head>
        <body>
            <h1>Top 3 Results</h1>
            <img src="data:image/png;base64,{img_base64}" alt="My Plot">
        </body>
        </html>
        """
        print("returning")
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
