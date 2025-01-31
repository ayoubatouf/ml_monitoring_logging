import numpy as np


def predict_lr(model, features):
    features = np.array(features).reshape(1, -1)
    predictions = model.predict(features)
    return predictions[0]
