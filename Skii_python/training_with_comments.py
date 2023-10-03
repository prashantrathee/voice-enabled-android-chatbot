# Importing the required libraries
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from keras.losses import categorical_crossentropy

# Initializing the WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Loading the intents from the JSON file
intents = json.loads(open('intents.json').read())

# Initializing the words, classes, documents, and ignore letters
words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# Looping through the intents and their patterns to extract the words, documents and classes
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatizing and removing ignore letters from words, sorting the words and classes alphabetically
print("words before lemmatizing = ", words)
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(list(set(words)))
print("words after lemmatizing = ", words)
classes = sorted(list(set(classes)))

# Creating the training set with bag of words and output rows
training = []
output_empty = [0] * len(classes)

# Looping through documents to create bags of words and output rows for each document
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize((word.lower())) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Shuffling the training set
random.shuffle(training)

# Converting training to numpy array and splitting into train_x and train_y
training = np.array(training)
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# Creating the neural network model with input, hidden, and output layers
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compiling the model with SGD optimizer and categorical_crossentropy loss function
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss=categorical_crossentropy, optimizer=sgd, metrics=['accuracy'])

# Fitting the model with the training data and saving the model, words, and classes to files
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=10, verbose=1)
model.save('skiimodel.h5', hist)
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Printing Done when training is complete
print("Done")