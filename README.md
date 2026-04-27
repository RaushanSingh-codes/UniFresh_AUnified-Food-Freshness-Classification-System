🍎 UniFresh – Food Freshness Detection Web App

📌 Overview

UniFresh is an AI-powered web application that detects whether a food item is Fresh or Spoiled using image classification.
It uses a trained deep learning model and provides instant predictions through a clean and interactive UI.

🚀 Features

🧠 Deep Learning based food classification

🖼 Upload image or use camera

⚡ Real-time prediction with confidence score

📜 Prediction history with interactive UI

🎨 Premium responsive frontend design

🔐 Authentication system (Login/Signup)

🛠 Tech Stack

Backend: Python, Flask

ML Model: TensorFlow / Keras

Frontend: HTML, CSS, JavaScript

Image Processing: OpenCV, Pillow

Deployment: Render / Railway

📂 Project Structure

UniFresh/ │ ├── models/ # Model loading files ├── routes/ # Flask routes (auth + main) ├── services/ # Prediction logic ├── utils/ # Image + GradCAM utilities │ ├── templates/ # HTML pages │ ├── index.html │ ├── login.html │ ├── signup.html │ └── history.html │ ├── static/ # CSS, uploads, heatmaps │ ├── app.py # Main Flask app ├── config.py # Config settings ├── requirements.txt ├── Procfile # Deployment config └── README.md 

⚙️ Installation & Run

git clone https://github.com/RaushanSingh-codes/UniFresh_AUnified-Food-Freshness-Classification-System.git cd UniFresh_AUnified-Food-Freshness-Classification-System pip install -r requirements.txt python app.py 

▶️ Usage

Open the web app

Upload an image or use camera

Click Scan

Get prediction: Fresh / Spoiled + Confidence

🧠 Model

Trained using food image dataset

Model file: final_food_freshness.keras

Loaded during runtime for predictions

🌐 Deployment

Deployed using Render

Use branch: Deploy

👥 Team

Raushan Kumar(2B)
Piyush Sengar(2B)
Mayank Sengar(@F)

📜 Note

This project is developed for academic and demonstration purposes.

⭐ Support

If you like this project, give it a ⭐ on GitHub.

