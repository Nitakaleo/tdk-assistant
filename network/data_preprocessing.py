import os

import nltk

import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle
import pickle
from network.utils import pos_tag_map

from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

lemmatizer = WordNetLemmatizer()

"""preprocessing in extracted words: lower case, lemmatization, remove duplicate, remove punctuation mark"""


def lemmatize_words(words_sequence):
    return [lemmatizer.lemmatize(w.lower(), pos_tag_map[p]) if pos_tag_map[p] is not None and w.isalpha()
            else lemmatizer.lemmatize(w.lower()) for w, p in pos_tag(words_sequence) if w.isalpha()]


def lemmatize_and_preprocess_words(words_list):
    """Filter punctuations marks, make in lower case and then lemmatize"""

    lemmatized_words = lemmatize_words(words_list)

    """remove duplicates"""
    return sorted(list(set(lemmatized_words)))


"""
load the dataset, intents.json and make preprocessing on data
like tokenization 
"""


def pattern_to_BoW(words_list_lemmatized, pattern, tokenized=True):
    BoW = []
    if not tokenized:
        pattern = word_tokenize(pattern)
        pattern = lemmatize_words(pattern)

        print("\n\nPATTERN: ", pattern, "\n\n")

    for w in words_list_lemmatized:
        BoW.append(1) if w in pattern else BoW.append(0)

    return BoW


def load_and_preprocess_data(intents):
    patterns_lemmatized = []
    words_list = []
    classes = []
    labels = []
    responses = []
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # use tokenization to extract words from a given pattern
            extracted_words = word_tokenize(pattern)
            # build list of the words
            words_list.extend(extracted_words)
            # save couple pattern and corresponding labels
            patterns_lemmatized.append(lemmatize_words(extracted_words))
            labels.append(intent['tag'])

        responses.append(intent['responses'])

        if intent['tag'] not in classes:
            classes.append(intent['tag'])
    classes = sorted(list(classes))
    words_list_lemmatized = lemmatize_and_preprocess_words(words_list)

    print("\nLEMMATIZED WORDS: ", words_list_lemmatized, "\n")

    if not os.path.isdir("model"):
        os.mkdir("model")

    pickle.dump(words_list_lemmatized, open('model/words_list_lemmatized.pickle', 'wb'))
    pickle.dump(classes, open('model/classes.pickle', 'wb'))

    return words_list_lemmatized, classes, patterns_lemmatized, labels


def get_train_and_test(json_intents_filename):
    # get preprocessed data

    words_list_lemmatized, classes, pattern_lemmatized, labels = load_and_preprocess_data(json_intents_filename)

    # create x_train and y_train
    x_train = []
    y_train = []

    # space for a row labels
    encoded_labels = np.zeros(len(classes))

    # training set, bag of words for each sentence
    for pattern, label in zip(pattern_lemmatized, labels):
        # create a bags of words
        BoW = pattern_to_BoW(words_list_lemmatized, pattern)

        x_train.append(BoW)
        # output is a '0' for each tag and '1' for current tag (for each pattern)
        aux_lab = list(encoded_labels)

        aux_lab[classes.index(label)] = 1

        y_train.append(aux_lab)

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    # shuffle data
    x_train, y_train = shuffle(x_train, y_train)
    # create train and test lists. X - patterns, Y - intents
    print("X_train, Y_train created correctly")

    print("X_train: ", x_train.shape)
    print("Y_train: ", y_train.shape)

    return x_train, y_train
