from flask import Flask, render_template, request, redirect, session
import tensorflow as tf
import numpy as np
from PIL import Image
import os, uuid, base64
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# -------------------- MODEL --------------------


model = tf.keras.models.load_model(
    "final_model.h5",
    compile=False,
    safe_mode=False
)

IMG_SIZE = (224, 224)
UPLOAD = "static/uploads"
os.makedirs(UPLOAD, exist_ok=True)

# -------------------- TEMP USERS --------------------
users = {}

# -------------------- PREPROCESS --------------------
def preprocess(path):
    img = Image.open(path).convert("RGB")
    img = img.resize(IMG_SIZE)
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# -------------------- PREDICTION --------------------
def predict_image(path):

    img = preprocess(path)
    pred = float(model.predict(img)[0][0])

    fresh = (1 - pred) * 100
    spoiled = pred * 100
    confidence = abs(pred - 0.5) * 2 * 100

    if confidence < 50:
        return "Not Identified", 0, 0, 0

    label = "Fresh" if pred < 0.5 else "Spoiled"

    return label, round(fresh,2), round(spoiled,2), round(confidence,2)

# -------------------- SIGNUP --------------------
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if u in users:
            return "User already exists"

        users[u] = p
        return redirect("/login")

    return render_template("signup.html")

# -------------------- LOGIN --------------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if u in users and users[u] == p:
            session["user"] = u
            return redirect("/")

        return "Invalid login"

    return render_template("login.html")

# -------------------- LOGOUT --------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------------------- HISTORY --------------------
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    history = session.get("history", [])[::-1]
    return render_template("history.html", history=history)

# -------------------- HOME --------------------
@app.route("/")
def index():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "index.html",
        prediction=session.get("prediction"),
        fresh=session.get("fresh", 0),
        spoiled=session.get("spoiled", 0),
        confidence=session.get("confidence", 0),
        image=session.get("image"),
        history=session.get("history", [])
    )

# -------------------- UPLOAD --------------------
@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect("/login")

    file = request.files.get("image")

    if not file or file.filename == "":
        return redirect("/")

    filename = str(uuid.uuid4()) + ".jpg"
    path = os.path.join(UPLOAD, filename)
    file.save(path)

    label, fresh, spoiled, confidence = predict_image(path)

    # SAVE RESULT
    session["prediction"] = label
    session["fresh"] = fresh
    session["spoiled"] = spoiled
    session["confidence"] = confidence
    session["image"] = path.replace("\\", "/")

    # HISTORY
    history = session.get("history", [])
    history.append({
        "image": session["image"],
        "prediction": label,
        "confidence": confidence
    })

    session["history"] = history[-10:]
    session.modified = True

    return redirect("/")

# -------------------- CAMERA --------------------
@app.route("/predict_camera", methods=["POST"])
def predict_camera():

    if "user" not in session:
        return redirect("/login")

    data = request.form.get("image_data")

    if not data:
        return redirect("/")

    filename = str(uuid.uuid4()) + ".jpg"
    path = os.path.join(UPLOAD, filename)

    image_data = base64.b64decode(data.split(",")[1])
    with open(path, "wb") as f:
        f.write(image_data)

    label, fresh, spoiled, confidence = predict_image(path)

    # SAVE RESULT
    session["prediction"] = label
    session["fresh"] = fresh
    session["spoiled"] = spoiled
    session["confidence"] = confidence
    session["image"] = path.replace("\\", "/")

    # HISTORY
    history = session.get("history", [])
    history.append({
        "image": session["image"],
        "prediction": label,
        "confidence": confidence
    })

    session["history"] = history[-10:]
    session.modified = True

    return redirect("/")

# -------------------- RUN --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    debug = os.environ.get("DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=port, debug=debug)