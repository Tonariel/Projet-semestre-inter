
from datetime import datetime

class Donnee:

    def __init__(self, date, heure, capteur, valeur):
        self.date = date
        self.heure = heure
        self.capteur = capteur
        self.valeur = valeur

    def afficher(self):
        print(self.date, self.heure, self.capteur, self.valeur)



donnees = []

with open("Data/aruba.txt", "r") as fichier:  ### changer pour avoir la fonction pour chaque txt d'un coup 
    
    for ligne in fichier:

        elements = ligne.split()
        
        if len(elements) < 4:
            continue

        try:
            datetime.strptime(elements[0], "%Y-%m-%d")
        except ValueError:
            continue
        
        date = elements[0]
        heure = elements[1]
        capteur = elements[2]
        valeur = elements[3]

        donnee = Donnee(date, heure, capteur, valeur)

        donnees.append(donnee)
        
        
for donnee in donnees:
    print(donnee.capteur, donnee.valeur)