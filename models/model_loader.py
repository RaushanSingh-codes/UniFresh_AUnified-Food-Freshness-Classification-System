import tensorflow as tf

def load_model():
    return tf.keras.models.load_model("final_food_freshness.keras")