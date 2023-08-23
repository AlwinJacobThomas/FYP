import pandas as pd
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

# Load the dataset

df = pd.read_csv('review-rating.csv', usecols=['review', 'rating'])

# Remove leading and trailing spaces from column names
df.columns = df.columns.str.strip()

# Convert the 'rating' column to integer
df['rating'] = df['rating'].astype(int)

# Split the dataset into training and testing sets
train_size = int(0.8 * len(df))
train_reviews = df['review'][:train_size]
train_ratings = df['rating'][:train_size]
test_reviews = df['review'][train_size:]
test_ratings = df['rating'][train_size:]

# Tokenize the text
tokenizer = Tokenizer(lower=True)
tokenizer.fit_on_texts(train_reviews)

# Convert text to sequences
train_sequences = tokenizer.texts_to_sequences(train_reviews)
test_sequences = tokenizer.texts_to_sequences(test_reviews)

# Pad sequences
max_sequence_length = max(len(seq) for seq in train_sequences)
train_sequences = pad_sequences(train_sequences, maxlen=max_sequence_length)
test_sequences = pad_sequences(test_sequences, maxlen=max_sequence_length)

num_classes = max(train_ratings.max(), test_ratings.max()) + 1
train_ratings = to_categorical(train_ratings, num_classes=num_classes)
test_ratings = to_categorical(test_ratings, num_classes=num_classes)

# Define the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(len(tokenizer.word_index) + 1, 128, input_length=max_sequence_length),
    tf.keras.layers.LSTM(128),
    tf.keras.layers.Dense(6, activation='softmax')
])

# Compile the model
# model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(train_sequences, train_ratings, epochs=5, validation_data=(test_sequences, test_ratings))

# Evaluate the model on the test set
_, accuracy = model.evaluate(test_sequences, test_ratings)
print('Test Accuracy:', accuracy)

 # Save the trained model
model.save('NewModel.h5')


# Define a new review
new_review = "he was a great doctor and have vast knowledge on his field of expertise"

# Tokenize and pad the new review sequence
new_sequences = tokenizer.texts_to_sequences([new_review])
new_sequences = pad_sequences(new_sequences, maxlen=max_sequence_length)

# Make predictions
predictions = model.predict(new_sequences)

# Get the predicted rating
predicted_rating = np.argmax(predictions) + 1

print('Predicted Rating:', predicted_rating)
