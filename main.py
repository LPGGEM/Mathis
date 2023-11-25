import math 
import os
from data import *

def term_frequency(chaine:str)->dict:
    """
    Fonction qui calcule la fréquence d'apparition de chaque caractère dans une chaîne de caractères
    """
    dict = {}
    for i in range(len(chaine)):
        if chaine[i] not in dict:
            dict[chaine[i]] = 1
        else:
            dict[chaine[i]] += 1
    return dict



def inverse_document_frequency(directory:str)->dict:
    """
    Écrire une fonction qui prend en paramètre le répertoire où se trouve l’ensemble des fichiers du corpus et qui retourne un dictionnaire associant à chaque mot son score IDF. 
    """
    num_files = 0
    word_counts = {}

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file:
            num_files += 1
            words = file.read().split()
            word_counts = term_frequency(words)

    for word in word_counts:
        word_counts[word] = math.log(num_files / word_counts[word])


    word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1]))

    return word_counts

def tf_idf_matrix(directory):
    idf_scores = inverse_document_frequency(directory)
    tf_idf_matrix = {}

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file:
            words = file.read().split()
            word_counts = {word: words.count(word) for word in words}
            total_words = len(words)
            try:
                tf_scores = {word: count / total_words for word, count in word_counts.items()}
                tf_idf_scores = {word: tf_scores[word] * idf_scores[word] for word in tf_scores}
                tf_idf_matrix[filename] = tf_idf_scores
            except:
                pass    

    return tf_idf_matrix

    

if __name__ == '__main__':
    cleaned_file()
    print(tf_idf_matrix("./cleaned"))
    print("hello")


