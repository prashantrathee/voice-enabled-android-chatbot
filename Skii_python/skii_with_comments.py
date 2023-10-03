Importing necessary libraries and modules
import random
import json
import pickle
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from keras.models import load_model

Downloading stopwords from NLTK
nltk.download('stopwords')

Defining the class for the chatbot
class skii:
    # Initializing class variables
    def init(self):
        self.hist = None
        self.intents = json.loads(open('intents.json').read()) # Loading intents from json file
        self.ERROR_THRESHOLD = 0.25 # Defining error threshold
        self.lemmatizer = WordNetLemmatizer() # Initializing WordNetLemmatizer object
        self.words = pickle.load(open('words.pkl', 'rb')) # Loading word tokens from pickle file
        self.classes = pickle.load(open('classes.pkl', 'rb')) # Loading class labels from pickle file
        self.basic_model = load_model('skiimodel.h5') # Loading pre-trained model from file
    # Function to clean up sentences
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence) # Tokenizing the sentence
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words] # Lemmatizing each word and converting to lowercase
        return sentence_words

    # Function to generate bag of words
    def bag_of_words(self, sentence, words_list):
        sentence_words = self.clean_up_sentence(sentence) # Cleaning up sentence
        bag = [0] * len(words_list) # Creating a bag of zeros
        for w in sentence_words:
            for i, word in enumerate(words_list):
                if word == w:
                    bag[i] = 1 # Setting the value to 1 for words that appear in the sentence
        return np.array(bag) # Converting bag to numpy array

    # Function to preprocess a sentence
    def preprocess(self, sentence):
        tokens = nltk.word_tokenize(sentence) # Tokenizing the sentence
        print("tokens before = ",tokens)
        
        # Lowercasing
        tokens = [token.lower() for token in tokens]
        
        # Stopword removal
        # stop_words = set(stopwords.words('english'))
        # tokens = [token for token in tokens if token not in stop_words]
        
        print("tokens after stopwords = ",tokens)
        # # Stemming
        # stemmer = PorterStemmer()
        # tokens = [stemmer.stem(token) for token in tokens]
        
        print("tokens now = ",tokens)

        # Remove punctuation
        tokens = [token for token in tokens if token.isalnum()]
        
        # Join the tokens back into a string
        print("tokens = ",tokens)
        preprocessed_sentence = ' '.join(tokens)
        
        return preprocessed_sentence

    # Function to predict the class of the sentence
    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence, self.words) # Generating bag of words for the sentence
        all_results = self.basic_model.predict(np.array([bow]))[0] # Predicting using the pre-trained model
        print(all_results.shape)
        results = [[i, r] for i, r in enumerate(all_results) if r > self.ERROR_THRESHOLD] # Selecting results above error threshold
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})

        return return_list
    
    def cosine_similarity_score(self, sentence, pattern):
        # Preprocess the sentences
        # Convert sentences to vectors using TfidfVectorizer
        vectorizer = TfidfVectorizer().fit_transform([sentence, pattern])

        # Calculate cosine similarity between the two vectors
        cosine_sim = cosine_similarity(vectorizer[0],vectorizer[1])[0][0]
        return cosine_sim
    
    def get_basic_questions_response(self, sentence, tag, patterns, responses):
        # Preprocess the input sentence
        print("without preprocessing = ",sentence)
        sentence = self.preprocess(sentence)

        # Calculate cosine similarity between the preprocessed input sentence and each pattern in the list
        pattern_cosine_distances = []
        for pattern in patterns:
            pattern_cosine_distances.append(self.cosine_similarity_score(sentence=sentence, pattern=pattern))

        # Get the maximum cosine similarity score and the corresponding index
        max_patttern_cosine = np.max(pattern_cosine_distances)
        cosine_max_pattern_indexes = [index for index,distance in enumerate(pattern_cosine_distances) if distance == max_patttern_cosine]

        # Select a response randomly from the list of responses with the highest cosine similarity score
        responses_array = responses[random.choice(cosine_max_pattern_indexes)]
        print("max index = ", cosine_max_pattern_indexes)
        print("cosine distances = ",pattern_cosine_distances)
        print("responses = ",responses_array)
        return random.choice(responses_array)
    
    def get_response(self, intents_list, sentence):
        result = ""
        print(intents_list)
        try:
            # Get the intent with the highest probability
            max_probability_tag = max(intents_list,key=lambda x: float(x['probability']))
            tag = max_probability_tag['intent']
            list_of_intents = self.intents['intents']

            # Check if the intent is of basic or non-basic type
            tag_type = tag[:5]
            found = False
            for i in list_of_intents:
                if i['tag'] == tag:
                    if tag_type == "basic":
                        # Call the get_basic_questions_response function to get a response for the input sentence
                        result = self.get_basic_questions_response(sentence=sentence, tag=tag, patterns=np.array(i['patterns']),responses=np.array(i['responses']))
                    else:
                        # Select a response randomly from the list of responses
                        result = random.choice(i['responses'])
                    found = True
                if found:
                    break
        except IndexError:
            result = "I don't understand !"
        print("returning = ",result)
        return result
    
    def predict(self, message):
        # Get the list of intents predicted for the input message
        print("Got message in predict = ",message)
        ints = self.predict_class(message)

        # Get a response for the input message using the get_response function
        res = self.get_response(ints, message)
        return res
