import tensorflow as tf

def graph_model(out_dim):
    return tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation="relu", input_shape=(32,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(1024, activation="relu"),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(2048, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(out_dim, activation="sigmoid")
    ])
