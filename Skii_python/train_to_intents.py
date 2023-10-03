import numpy as np
import json
import re
import yaml
import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords

basic_structure = {
        "tag":"",
        "patterns":[],
        "responses":[],
        "context_set":""
    }

def remove_stopwords(input_string):
    stop_words = set(stopwords.words('english'))
    # Stopword removal
    tokens = nltk.word_tokenize(input_string)
    tokens = [token for token in tokens if token not in stop_words or token =="you" or token == "not"]
    
    print("before stopwords ",input_string)
    input_string = ' '.join(tokens)
    print("after stopwords",input_string)
    return input_string


def clean_strings(input_string):
    # Remove double quotes
    cleaned_string = input_string.replace('""', '')

    # Replace inner double quotes with single quotes
    cleaned_string = cleaned_string.replace('"', "'")

    # # Remove all non-alphanumeric characters
    cleaned_string = re.sub('[^0-9a-zA-Z\[\]0-9,.?]+', ' ', cleaned_string)

    # Replace '[' and ']' with '--'
    cleaned_string = cleaned_string.replace('[', '---').replace(']', '---')
    return cleaned_string

def add_to_intents(to_add):
    with open('intents.json','r') as r:
        all_intents = json.load(r)
        all_intents['intents'].append(to_add)
    with open('intents.json','w') as f:
        json.dump(all_intents,f,indent=4)
def train_jokes(jokes):

    jokes_list = jokes.iloc[:300].values.tolist()
    jokes_result = []
    for i in range(300):
        cleaned_joke = clean_strings(jokes_list[i][1])
        jokes_result.append(cleaned_joke)

    jokes_structure = {"tag": "jokes",
            "patterns": ["Tell me a joke","How about a joke","Give me a joke","Feeling funny","I want to feel good","I am feeling down","Feeling sad"],
            "responses": [jokes_result],
            "context_set": ""
        }
    all_intents = {}
    with open('intents.json','r') as r:
        all_intents = json.load(r)
        all_intents['intents'].append(jokes_structure)
    with open('intents.json','w') as f:
        json.dump(all_intents,f,indent=4)  
    


# jokes = pd.read_csv('shortjokes.csv')
# print(jokes)

def train_movies(movies):
    
    sorted_movies = movies.sort_values('Rating',ascending=False)
    sorted_list = sorted_movies.iloc[:300].values.tolist()
    name_index = 0
    year_index = 1
    rating_index = 7
    summary_index = 3
    print(sorted_list[0][3])
    selected_movies = []
    for i in range(300):
        tempMovie = sorted_list[i]
        movieInfo = f"Name : {clean_strings(tempMovie[name_index])} \nYear : {clean_strings(tempMovie[year_index])} \nRating : {clean_strings(tempMovie[rating_index])} \nSummary : {clean_strings(tempMovie[summary_index])}\n"
        selected_movies.append(movieInfo)

    movies_list = {"tag": "movies",
                    "patterns":["What are some good movies","How about you suggest me a good movie","Suggest a good movie","A good movie"],
                    "responses":selected_movies,
                    "context_set": ""
                    }
    all_intents = {}
    add_to_intents(movies_list)


# movies = pd.read_csv('movie_hydra.csv')

# train_movies(movies=movies)

def train_conversations(file_path,tag):
    print("file path = ",file_path)
    with open(file_path,'r') as f:
        lines = yaml.load(f,Loader=yaml.FullLoader)
    patterns_list = []
    responses_list = []
    for i,line in enumerate(lines['conversations']):
        patterns_list.append(clean_strings(line[0]))
        responses_list.append(clean_strings(line[1]))
    basic_structure["patterns"] = patterns_list
    basic_structure["responses"] = responses_list
    basic_structure['tag'] = tag
    # add_to_intents(basic_structure)
    print(basic_structure)


def train_conversations_ai():
    file_path = "conversation_basic/ai.yml"
    train_conversations(file_path=file_path, tag="basicQA")


def train_conversations_profile():
    file_path = "conversation_basic/botprofile.yml"
    train_conversations(file_path=file_path, tag="basicProfile")
    

# train_conversations_profile()
def train_conversations_computer():
    file_path = "conversation_basic/computers.yml"
    train_conversations(file_path=file_path,tag="basicComputers")

def train_conversations_emotions():
    file_path = "conversation_basic/emotion.yml"
    with open(file_path,'r') as f:
        lines = yaml.load(f,Loader=yaml.FullLoader)
    patterns_list = []
    responses_list = []
    for i,line in enumerate(lines['conversations']):
        removed_stopwords_pattern = remove_stopwords(line[0])
        patterns_list.append(clean_strings(removed_stopwords_pattern))
        one_response_list = []
        for response in line[1:]:
            one_response_list.append(clean_strings(response))
        responses_list.append(one_response_list)
    print("patterns = ",patterns_list)
    print("responses = ",responses_list)
    basic_structure["patterns"] = patterns_list
    basic_structure['responses'] = responses_list
    basic_structure["tag"] = "basicEmotions"
    # add_to_intents(basic_structure)
    print(basic_structure)


train_conversations_emotions()
def train_conversations_array(file_path,tag):
    # file_path = "conversation_basic/food.yml"
    with open(file_path,'r') as f:
        lines = yaml.load(f,Loader=yaml.FullLoader)
    print("lines = ",lines)
    patterns_list = []
    responses_list = []
    for i,line in enumerate(lines['conversations']):
        # print("\n\nline = ",line)
        # print("pattern list = ",patterns_list)
        # print("responses list = ",responses_list)
        # print(" line [0] = ",line[0])
        removed_stopwords_pattern = remove_stopwords(line[0])
        cleaned_pattern = clean_strings(removed_stopwords_pattern)
        cleaned_response = clean_strings(line[1])
        if((cleaned_pattern in np.array(patterns_list))==True):
            # print("true for ",cleaned_pattern," and found in pattern list = ",patterns_list)
            index_of_pattern = np.where(np.array(patterns_list) == cleaned_pattern)[0][0]
            # print("\n\nindex found = ",index_of_pattern)
            responses_list[index_of_pattern].append(clean_strings(cleaned_response))
        else:
            patterns_list.append(clean_strings(cleaned_pattern))
            responses_list.append([cleaned_response])
    print("patterns = ",patterns_list)
    print("responses = ",responses_list)
    basic_structure["patterns"] = patterns_list
    basic_structure['responses'] = responses_list
    basic_structure["tag"] = tag
    # add_to_intents(basic_structure)
    print(basic_structure)


def train_basic_txt(file_path,tag):
    with open(file_path,'r') as file:
        conversation = file.readlines()
    # print(conversation)
    patterns = []
    responses = []
    for line in conversation:
        parts = line.split("\t")
        cleaned_pattern = clean_strings(parts[0])
        cleaned_response = clean_strings(parts[1])
        if((cleaned_pattern in np.array(patterns))==True):
            # print("true for ",cleaned_pattern," and found in pattern list = ",patterns)
            index_of_pattern = np.where(np.array(patterns) == cleaned_pattern)[0][0]
            # print("\n\nindex found = ",index_of_pattern)
            responses[index_of_pattern].append(clean_strings(cleaned_response))
        else:
            patterns.append(clean_strings(cleaned_pattern))
            responses.append([cleaned_response])
    
    print("patterns = ",patterns)
    # print("responses = ",responses)
    basic_structure['patterns'] = patterns
    basic_structure['responses'] = responses
    basic_structure['tag'] = tag
    add_to_intents(basic_structure)


# train_basic_txt("./basic_dialogues/basic_dialogs.txt","basicQATalk")
# train_conversations_emotions()

# train_conversations_array("conversation_basic/psychology.yml","basicPsychology")


# def train_large_data(file_path): 
#     train_file = json.loads(open(file_path).read())
#     print(train_file['data'][])




# train_large_data('SQUAD/train-v2.0.json')

