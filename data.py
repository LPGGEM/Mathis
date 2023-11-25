import os

def list_of_files(directory, extension):
    """
    Cette fonction retourne la liste des noms de fichiers se terminant par l'extension donnée dans un répertoire donné.
    
    Paramètres :
    directory (str) : Le chemin du répertoire contenant les fichiers à analyser.

    Retourne :
    list : Une liste de noms de fichiers se terminant par l'extension donnée.
    
    """

    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

files = list_of_files('speeches/', '.txt')

def get_president_name(file):
    """
    
    Cette fonction retourne le nom du président à partir du nom du fichier.

    Paramètres :
    file (str) : Le nom du fichier à analyser.

    Retourne :
    str : Le nom du président.
    
    """

    file = file[11:-4]

    if (file[-1].isdigit()):
        file = file[:-1]

    return file

president_surname = { 'Chirac': "Jacques", "Giscard d'Estaing": "Valérie", 'Hollande': "François", "Macron": "Emmanuel", "Mitterand": "François", "Sarkozy": "Nicolas" }


def get_president_surname(name):
    """
    Cette fonction retourne le nom de famille du président à partir du nom du président.

    Paramètres :
    name (str) : Le nom du président à analyser.

    Retourne :
    str : Le nom de famille du président.
    
    """

    return president_surname[name]


def print_president_list():
    """   
    Cette fonction affiche la liste des présidents à partir des noms des fichiers.
    """

    last = ""
    for i in files:
        txt = get_president_name(i)
        if (txt != last):
            print(txt)
            last = txt

def cleaned_file():
    """
    
    Cette fonction nettoie les fichiers du répertoire speeches et les écrit dans le répertoire cleaned.

    """
    ecrit = {'ç': 'c', 'é': 'e', 'è': 'e', 'ê': 'e', 'à': 'a', 'â': 'a', 'ù': 'u', 'û': 'u', 'î': 'i', 'ï': 'i', 'ô': 'o', 'ö': 'o', 'œ': 'oe', 'ç': 'c', 'É': 'E', 'È': 'E', 'Ê': 'E', 'À': 'A', 'Â': 'A', 'Ù': 'U', 'Û': 'U', 'Î': 'I', 'Ï': 'I', 'Ô': 'O', 'Ö': 'O', 'Œ': 'OE'}
    for i in files:
        f = open(f"speeches/{i}", 'r', encoding='utf-8')
        lower = f.read().lower()

        writed = open(f"cleaned/{i}", 'w', encoding='utf-8')
        #remplace les ' par des espaces
        lower = lower.replace("'", ' ')
        lower = lower.replace("-", ' ')
        lower = lower.replace("!", ' ')
        for key, value in ecrit.items():
            lower = lower.replace(key, value)
        #remplace les espaces multiples par un seul espace
        lower = ' '.join(lower.split())
        encoded = lower.encode('ascii', 'ignore')
        writed.write(encoded.decode())