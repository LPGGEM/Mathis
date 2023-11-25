import math 
import os
from data import *
import numpy as np

def term_frequency(chaine:str)->dict:
    """
    Fonction qui calcule la fréquence d'apparition de chaque caractère dans une chaîne de caractères

    Paramètres :
    chaine (str) : La chaîne de caractères à analyser.

    Retourne :
    dict : Un dictionnaire associant à chaque caractère sa fréquence d'apparition.
    """
    frequency = {}
    for i in range(len(chaine)):
        if chaine[i] not in frequency:
            frequency[chaine[i]] = 1
        else:
            frequency[chaine[i]] += 1

    frequency = dict(sorted(frequency.items(), key=lambda item: item[0]))
    return frequency



def inverse_document_frequency(directory:str)->dict:
    """
    Écrire une fonction qui prend en paramètre le répertoire où se trouve l’ensemble des fichiers du corpus et qui retourne un dictionnaire associant à chaque mot son score IDF.

    Paramètres :
    directory (str) : Le chemin du répertoire contenant les fichiers à analyser.

    Retourne :
    dict : Un dictionnaire associant à chaque mot son score IDF. 
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

    word_counts = dict(sorted(word_counts.items(), key=lambda item: item[0]))

    return word_counts

def tf_idf_matrix(directory:str)->list(dict()):
    """
    Cette fonction calcule la matrice TF-IDF pour un ensemble de fichiers dans un répertoire donné.

    Paramètres :
    directory (str) : Le chemin du répertoire contenant les fichiers à analyser.

    Retourne :
    list : Une liste de dictionnaires, où chaque dictionnaire contient les scores TF-IDF pour chaque mot dans un fichier.
    """
    idf_scores = inverse_document_frequency(directory)
    tf_idf_matrix = []

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file:
            namefile = filename.split(".")[0]
            tf_scores = term_frequency(file.read().split())
            tf_idf_scores = {}
            for word in tf_scores:
                try:
                    if tf_scores[word] != 1:
                        continue
                    tf_idf_scores[word] = tf_scores[word] * idf_scores[word]
                except:
                    pass
            tf_idf_matrix.append(tf_idf_scores)

    return tf_idf_matrix
        

    

if __name__ == '__main__':
    cleaned_file()
    matrix = tf_idf_matrix("./cleaned")
    print(matrix)


