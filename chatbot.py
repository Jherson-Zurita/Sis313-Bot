import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatizer = WordNetLemmatizer()

#Importamos los archivos generados en el código anterior
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

#Pasamos las palabras de oración a su forma raíz
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#Convertimos la información a unos y ceros según si están presentes en los patrones
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i]=1
    print(bag)
    return np.array(bag)

#Predecimos la categoría a la que pertenece la oración
# Modifica la función predict_class
def predict_classes(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    classes_pred = [classes[i] for i in range(len(res)) if res[i] > 0.23]  # Ajusta el umbral según sea necesario
    return classes_pred


#Obtenemos una respuesta aleatoria
# Modifica la función get_response
def get_responses(tags, intents_json, user_input):
    responses = []
    list_of_intents = intents_json['intents']

    for tag in tags:
        for i in list_of_intents:
            if i["tag"] == tag:
                responses.append(random.choice(i['responses']))
                break

    return responses


#Ejecutamos el chat en bucle
# Modifica el bucle principal
# Modifica el bucle principal

