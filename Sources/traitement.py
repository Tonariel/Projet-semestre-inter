import pandas as pd
from pathlib import Path



from datetime import datetime
chemin = Path(__file__).resolve().parent.parent / "Data" / "aruba.txt"

class Donnee:

    def __init__(self, timestamp, capteur, valeur):
        self.timestamp = timestamp
        self.capteur = capteur
        self.valeur = valeur

    def afficher(self):
        print(self.timestamp, self.capteur, self.valeur)



donnees = []

with open(chemin, "r") as fichier:
    for ligne in fichier:

        elements = ligne.split()
        
        if len(elements) < 4:
            continue

        try:
            timestamp = elements[0] + " " + elements[1]
        except ValueError:
            continue
        
        
        capteur = elements[2]
        valeur = elements[3]

        donnee = Donnee(timestamp, capteur, valeur)

        donnees.append(donnee)
donnee = Donnee(timestamp, capteur, valeur)





df = pd.DataFrame([
    {
        "timestamp": d.timestamp,
        "capteur": d.capteur,
        "valeur": d.valeur
    }
    
    for d in donnees
])


# Conversion groupée des timestamps
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="%Y-%m-%d %H:%M:%S.%f",
    errors="coerce"
)


# On supprime uniquement les dates invalides
df = df.dropna(subset=["timestamp"])

df = df.set_index("timestamp")



# Première date disponible
debut = df.index.min()

# Durée de la fenêtre
duree = pd.Timedelta(minutes=30)

# Fin de la fenêtre
fin = debut + duree

# Récupération des données
fenetre = df.loc[
    (df.index >= debut) &
    (df.index < fin)
]

nombre_capteurs = fenetre["capteur"].nunique()

nombre_lignes = len(fenetre)

# Nombre de capteurs différents
nombre_capteurs = fenetre["capteur"].nunique()

print("Nombre de lignes :", nombre_lignes)
print("Nombre de capteurs différents :", nombre_capteurs)

#### time stampe                fais 
#### combien                    fais 
#### piecce dominante           pas encore  
### temps (30m )                pour le moment 30m