import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


def train_model():
    # Load the dataset
    df = pd.read_csv('docops/doctor_reviews.csv')

    # Encode the target variable
    df['tag'] = df['tag'].map({'negative': 0, 'positive': 1})

    # Split the dataset into training and testing sets
    train_size = int(0.8 * len(df))
    train_reviews = df['review'][:train_size]
    train_tags = df['tag'][:train_size]
    test_reviews = df['review'][train_size:]
    test_tags = df['tag'][train_size:]

    # Tokenize the text
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(train_reviews)

    # Convert text to sequences
    train_sequences = tokenizer.texts_to_sequences(train_reviews)
    test_sequences = tokenizer.texts_to_sequences(test_reviews)

    # Pad sequences
    max_sequence_length = max(len(seq) for seq in train_sequences)
    train_sequences = pad_sequences(train_sequences, maxlen=max_sequence_length)
    test_sequences = pad_sequences(test_sequences, maxlen=max_sequence_length)

    # Define the model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Embedding(len(tokenizer.word_index) + 1, 128, input_length=max_sequence_length),
        tf.keras.layers.LSTM(128),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(train_sequences, train_tags, epochs=5, validation_data=(test_sequences, test_tags))

    # Save the trained model
    model.save('docops/sentiment_model.h5')


def load_model():
    # Load the pre-trained model
    model = tf.keras.models.load_model('docops/sentiment_model.h5')
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([''])  # Dummy fit to avoid errors during prediction
    return model, tokenizer


def predict_star_rating(new_review, model, tokenizer):
    print(new_review)
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
# model, tokenizer = load_model()

# Example usage
# new_review = "i am so satisfied.Great way of talking and good communication skill of the doctor"
# predicted_rating = predict_star_rating(new_review, model, tokenizer)

# if predicted_rating > 0.5:
#     print("Positive")
# else:
#     print("Negative")

# print(f'Predicted Star Rating: {predicted_rating}')
