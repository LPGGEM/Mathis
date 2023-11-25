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

def tf_idf_matrix(directory:str)->list:
    """
    Écrire une fonction qui prend en paramètre le répertoire où se trouve l’ensemble des fichiers du corpus et qui retourne une liste de listes représentant la matrice TF-IDF.

    Paramètres :
    directory (str) : Le chemin du répertoire contenant les fichiers à analyser.

    Retourne :
    list : Une liste de listes représentant la matrice TF-IDF.
    """
    idf_scores = inverse_document_frequency(directory)
    tf_idf_matrix = []
    tf_idf_dict = {}

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file:
            tf_scores = term_frequency(file.read().split())
            tf_idf_scores = []
            tf_idf_scores_dict = {}
            for word in tf_scores:
                try:
                    #? Si le mot n'est pas unique on passe au suivant
                    # if tf_scores[word] != 1:
                    #     continue
                    tf_idf_scores.append(tf_scores[word] * idf_scores[word])
                    tf_idf_scores_dict[word] = tf_scores[word] * idf_scores[word]
                except:
                    pass
            tf_idf_matrix.append(tf_idf_scores)
            tf_idf_dict[filename] = tf_idf_scores_dict

    return tf_idf_matrix, tf_idf_dict
        
def analyse_tf_idf(tf_idf_dict):
    # 1. Afficher la liste des mots les moins importants dans le corpus de documents.
    least_important_words = [word for document in tf_idf_dict for word, tf_idf_score in tf_idf_dict[document].items() if tf_idf_score < 0]
    # enlève si ya des doublons
    least_important_words = list(dict.fromkeys(least_important_words))
    print("Mots les moins importants : ", least_important_words)

    # 2. Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé
    highest_tf_idf_score = max(tf_idf_score for document in tf_idf_dict for tf_idf_score in tf_idf_dict[document].values())
    highest_tf_idf_words = [word for document in tf_idf_dict for word, tf_idf_score in tf_idf_dict[document].items() if tf_idf_score == highest_tf_idf_score]
    print("Mots avec le score TF-IDF le plus élevé : ", highest_tf_idf_words)

    # 3. Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac
    chirac_documents = [document for document in tf_idf_dict if "Chirac" in document]
    chirac_most_repeated_words = [max(tf_idf_dict[document], key=tf_idf_dict[document].get) for document in chirac_documents]
    print("Mots les plus répétés par le président Chirac : ", chirac_most_repeated_words)

    # 4. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois
    presidents_mentioned_nation = [get_president_name(document) for document in tf_idf_dict if 'Nation' in tf_idf_dict[document]]
    print("Présidents qui ont parlé de la Nation : ", presidents_mentioned_nation)

    # 5. Indiquer le premier président à parler du climat et/ou de l’écologie
    first_president_to_mention_climate = next((get_president_name(document) for document in tf_idf_dict if 'climat' in tf_idf_dict[document] or 'écologie' in tf_idf_dict[document]), None)
    print("Premier président à parler du climat ou de l'écologie : ", first_president_to_mention_climate)

    # 6. Hormis les mots dits « non importants », quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués.
    words_mentioned_by_all_presidents = [word for word in tf_idf_dict[next(iter(tf_idf_dict))] if all(word in tf_idf_dict[document] for document in tf_idf_dict) and any(tf_idf_dict[document][word] != 0 for document in tf_idf_dict)]
    print("Mots évoqués par tous les présidents : ", words_mentioned_by_all_presidents)

if __name__ == '__main__':
    cleaned_file()

    _, tf_idf_dict = tf_idf_matrix("./cleaned")
    analyse_tf_idf(tf_idf_dict)


