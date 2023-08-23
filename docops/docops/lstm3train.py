import pandas as pd
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences




def load_model():
    # Load the pre-trained model
    model = tf.keras.models.load_model('docops/NewModel.h5')
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([''])  # Dummy fit to avoid errors during prediction
    return model, tokenizer


def predict_star_rating(new_review, model, tokenizer):
    # Tokenize and pad the new review sequence
    new_sequences = tokenizer.texts_to_sequences([new_review])
    new_sequences = pad_sequences(new_sequences, maxlen=model.input_shape[1])

    # Make predictions
    predictions = model.predict(new_sequences)
    print(f'===>{predictions[0][0]}')
    # Return the predicted star rating
    return predictions[0][0]


# Train the model (run this once or whenever you want to retrain the model)
# train_model()

# Load the pre-trained model
model, tokenizer = load_model()

# Example usage
# new_review = "i am so satisfied.Great way of talking and good communication skill of the doctor"
# predicted_rating = predict_star_rating(new_review, model, tokenizer)

# if predicted_rating > 0.5:
#     print("Positive")
# else:
#     print("Negative")

# print(f'Predicted Star Rating: {predicted_rating}')
