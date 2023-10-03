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

nltk.download('stopwords')


class skii:
    def __init__(self):
        self.hist = None
        self.intents = json.loads(open('intents.json').read())
        self.ERROR_THRESHOLD = 0.25
        self.lemmatizer = WordNetLemmatizer()
        self.words = pickle.load(open('words.pkl', 'rb'))
        self.classes = pickle.load(open('classes.pkl', 'rb'))
        self.basic_model = load_model('skiimodel.h5')

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence, words_list):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(words_list)
        for w in sentence_words:
            for i, word in enumerate(words_list):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def preprocess(self, sentence):
        tokens = nltk.word_tokenize(sentence)
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

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence, self.words)
        all_results = self.basic_model.predict(np.array([bow]))[0]
        print(all_results.shape)
        results = [[i, r] for i, r in enumerate(all_results) if r > self.ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})

        return return_list

    def cosine_similarity_score(self, sentence, pattern):
        # Preprocess the sentences
        # Convert sentences to vectors
        vectorizer = TfidfVectorizer().fit_transform([sentence, pattern])

        # Calculate cosine similarity
        cosine_sim = cosine_similarity(vectorizer[0],vectorizer[1])[0][0]
        return cosine_sim

    def get_basic_questions_response(self, sentence, tag, patterns, responses):
        print("without preprocessing = ",sentence)
        sentence = self.preprocess(sentence)
        pattern_cosine_distances = []
        for pattern in patterns:
            pattern_cosine_distances.append(self.cosine_similarity_score(sentence=sentence, pattern=pattern))
        max_patttern_cosine = np.max(pattern_cosine_distances)
        cosine_max_pattern_indexes = [index for index,distance in enumerate(pattern_cosine_distances) if distance == max_patttern_cosine]
        print("max index = ", cosine_max_pattern_indexes)
        print("cosine distances = ",pattern_cosine_distances)
        responses_array = responses[random.choice(cosine_max_pattern_indexes)]
        print("responses = ",responses_array)
        # response_consine_distances = []
        # for response in responses_array:
        #     response_consine_distances.append(self.cosine_similarity_score(sentence=sentence,pattern=response))
        # max_response_cosine = np.max(response_consine_distances)
        # cosine_max_response_indexes = [max_index for max_index, distance in enumerate(response_consine_distances) if distance == max_response_cosine]
        return random.choice(responses_array)

    def get_response(self, intents_list, sentence):
        result = ""
        print(intents_list)
        try:
            max_probability_tag = max(intents_list,key=lambda x: float(x['probability']))
            tag = max_probability_tag['intent']
            list_of_intents = self.intents['intents']
            tag_type = tag[:5]
            found = False
            for i in list_of_intents:
                if i['tag'] == tag:
                    if tag_type == "basic":
                        result = self.get_basic_questions_response(sentence=sentence, tag=tag, patterns=np.array(i['patterns'],dtype="object"),responses=np.array(i['responses'],dtype="object"))
                    else:                    
                        result = random.choice(i['responses'])
                    found = True
                if found:
                    break
        except IndexError:
            result = "I don't understand !"
        print("returning = ",result)
        return result

    def predict(self, message):
        print("Got message in predict = ",message)
        ints = self.predict_class(message)
        res = self.get_response(ints, message)
        return res


    

