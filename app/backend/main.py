import uvicorn
import json
import requests
import numpy as np
import tensorflow as tf
from io import BytesIO
from tensorflow import keras
from fastapi import FastAPI
from PIL import Image
from pydantic import BaseModel

race_file = open('race_names.json', 'r')
race_names = json.load(race_file)

image_size = (180, 180)

app = FastAPI()

model = keras.models.load_model('naive_model')


@app.get("/prediction")
def get_prediction(q: str):
    response = requests.get(q)
    img = Image.open(BytesIO(response.content)).resize((180, 180))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)

    top4 = predictions.argsort()[0, -1:-5:-1]

    breakdown = []
    for race, acc in zip(np.array(race_names)[top4], predictions[0, top4]):
        breakdown.append(f'{race} at {acc:.2%}')
    return breakdown


if __name__ == "__main__":
    uvicorn.run("fastapi:app")
