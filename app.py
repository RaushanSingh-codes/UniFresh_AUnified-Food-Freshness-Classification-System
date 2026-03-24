from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Load trained model
model = tf.keras.models.load_model("final_food_freshness.keras/")


# Image preprocessing according to your model
def preprocess_image(image_path):

    img = Image.open(image_path).convert("RGB")

    img = img.resize((224,224))

    img = np.array(img)

    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    return img


def predict_image(image_path):

    img = preprocess_image(image_path)

    prediction = model.predict(img)

    confidence = float(prediction[0][0])

    if confidence > 0.5:
        label = "Spoiled"
    else:
        label = "Fresh"

    return label, confidence


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return "No file uploaded"

    file = request.files["image"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    label, confidence = predict_image(filepath)

    return render_template(
        "index.html",
        prediction=label,
        confidence=round(confidence*100,2),
        image_path=filepath
    )


if __name__ == "__main__":
    app.run(debug=True)