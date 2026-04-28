import tensorflow as tf
import numpy as np
from PIL import Image

IMG_SIZE = (224, 224)


model = tf.keras.models.load_model(
    "final_food_freshness.keras",
    compile=False,
    safe_mode=False
)


def preprocess(path):
    img = Image.open(path).convert("RGB")
    img = img.resize(IMG_SIZE)
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def predict_image(path):

    img = preprocess(path)

    pred = float(model.predict(img)[0][0])

    fresh = (1 - pred) * 100
    spoiled = pred * 100

    confidence = abs(pred - 0.5) * 2 * 100

    # NOT IDENTIFIED
    if confidence < 50:
        return "Not Identified", 0, 0

    label = "Fresh" if pred < 0.5 else "Spoiled"

    return label, round(fresh, 2), round(spoiled, 2)