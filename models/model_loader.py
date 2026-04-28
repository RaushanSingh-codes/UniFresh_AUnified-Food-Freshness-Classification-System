import tensorflow as tf

def load_model():
    print("🔥 Loading ML model...")
    return tf.keras.models.load_model(
    "final_model.h5",
    compile=False,
    safe_mode=False
)