from flask import Blueprint, render_template, request, session, redirect, current_app
from PIL import Image
import os, uuid, base64

from services.prediction_service import predict_image

main = Blueprint("main", __name__)

UPLOAD = "static/uploads"
os.makedirs(UPLOAD, exist_ok=True)


# ---------------- HOME ----------------
@main.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    return render_template(
        "index.html",
        count=session.get("count", 0),
        prediction=session.get("prediction"),
        confidence=session.get("confidence"),
        level=session.get("level"),
        image=session.get("image")
    )


# ---------------- UPLOAD ----------------
@main.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    file = request.files.get("image")

    if not file or file.filename == "":
        return "No file selected"

    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return "Invalid file type"

    filename = str(uuid.uuid4()) + ".jpg"
    path = os.path.join(UPLOAD, filename)

    try:
        file.save(path)

        img = Image.open(path).convert("RGB")

        model = current_app.config["MODEL"]

        label, confidence, level = predict_image(model, img)

        # 🔥 SAVE
        session["prediction"] = label
        session["confidence"] = round(confidence, 2)
        session["level"] = level
        session["image"] = path.replace("\\", "/")

        session["count"] = session.get("count", 0) + 1

    except Exception as e:
        return f"Error: {str(e)}"

    return redirect("/")

# ---------------- HISTORY -- --------------
@main.route("/history")
def history():

    if "user" not in session:
        return redirect("/login")

    history = session.get("history", [])

    history = history[::-1]

    return render_template("history.html", history=history)


# ---------------- CAMERA ----------------
@main.route("/predict_camera", methods=["POST"])
def predict_camera():

    if "user" not in session:
        return redirect("/login")

    data = request.form.get("image_data")

    if not data:
        return "No camera data received"

    filename = str(uuid.uuid4()) + ".jpg"
    path = os.path.join(UPLOAD, filename)

    try:
        # 🔥 base64 decode
        image_data = base64.b64decode(data.split(",")[1])

        with open(path, "wb") as f:
            f.write(image_data)

        img = Image.open(path).convert("RGB")

        model = current_app.config["MODEL"]

        # 🔥 prediction
        label, confidence, level = predict_image(model, img)

        # 🔥 SAVE
        session["prediction"] = label
        session["confidence"] = round(confidence, 2)
        session["level"] = level
        session["image"] = path.replace("\\", "/")

        session["count"] = session.get("count", 0) + 1

    except Exception as e:
        return f"Camera Error: {str(e)}"

    return redirect("/")