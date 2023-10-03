# Android Speech Recognizable Chatbot with Flask API

This repository contains the code for an Android chatbot application that utilizes speech recognition and predicts the class of a user query. The chatbot generates responses based on the predicted class and provides a seamless conversational experience. The application communicates with a Flask API running on localhost, which handles the prediction and response generation.

## Features

- Speech recognition: The chatbot can understand user input through speech.
- Query prediction: The application predicts the class of the user's query.
- Response generation: Based on the predicted class, the chatbot generates relevant responses.
- Android interface: The chatbot has a user-friendly Android interface.
- Local Flask API: Communication between the Android app and the prediction model is facilitated by a Flask API running on localhost.

## Setup

### Android Application Setup

1. Clone this repository to your local machine.

2. Open the Skii_android using Android Studio.

3. Configure the necessary permissions for speech recognition in the `AndroidManifest.xml` file.

4. Build and install the Android application on your device.

### Flask API Setup

1. Navigate to the `Skii_python` directory.

2. Create a virtual environment (recommended) using the following commands:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```

4. Run the Flask API using:
   ```
   python main.py
   ```


### Training Data

1. Training data is given in the Skii_python directory.  The data is categorized into different classes that represent the different types of queries the chatbot will handle.

2. Train a classification model using your selected training data. Save the trained model as a serialized file (e.g., `.pkl` or `.h5`).

3. Replace the placeholder model in the Flask API code (`main.py`) with your trained model.

## Usage

1. Open the Android application on your device.

2. Grant the necessary permissions for speech recognition when prompted.

3. Speak a query into the application. The speech will be converted to text and sent to the Flask API for prediction.

4. The Flask API will predict the class of the query and generate a response based on the predicted class.

5. The response will be displayed on the Android application's interface as a chat message.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the chatbot's functionality, feel free to submit a pull request.

