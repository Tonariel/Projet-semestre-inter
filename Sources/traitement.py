import pandas as pd
from pathlib import Path
from typing import Optional



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


def informations_fenetres(
    dataframe: pd.DataFrame,
    duree_frame: pd.Timedelta
) -> list[tuple[float, int, Optional[str], float]]:
    if not isinstance(dataframe.index, pd.DatetimeIndex):
        raise ValueError("Le DataFrame doit avoir un DatetimeIndex.")

    duree = pd.Timedelta(duree_frame)
    if duree <= pd.Timedelta(0):
        raise ValueError("La durée d'une fenêtre doit être positive.")

    if dataframe.empty:
        return []

    dataframe = dataframe.sort_index()
    debut = dataframe.index.min().normalize()
    resultats = []
    capteurs_actifs = {}
    intervalles = []

    def salle_du_capteur(capteur: str) -> Optional[str]:
        if capteur.endswith(("D001", "D002")):
            return "Dehors"
        return MAPPING_CAPTEURS_aruba.get(capteur)

    for timestamp, capteur, valeur in dataframe[
        ["capteur", "valeur"]
    ].itertuples(index=True, name=None):
        valeur = str(valeur).strip().upper()
        if not isinstance(capteur, str):
            continue

        if valeur.startswith(("ON", "OPEN")):
            capteurs_actifs.setdefault(capteur, timestamp)
        elif valeur.startswith(("OFF", "CLOSE")):
            debut_capteur = capteurs_actifs.pop(
                capteur,
                debut + ((timestamp - debut) // duree) * duree,
            )
            salle = salle_du_capteur(capteur)
            if salle is not None and timestamp > debut_capteur:
                intervalles.append((debut_capteur, timestamp, salle))

    fin_derniere_fenetre = (
        debut
        + ((dataframe.index.max() - debut) // duree + 1) * duree
    )
    for capteur, debut_capteur in capteurs_actifs.items():
        salle = salle_du_capteur(capteur)
        if salle is not None:
            intervalles.append(
                (debut_capteur, fin_derniere_fenetre, salle)
            )

    durees_fenetres = {}
    for debut_intervalle, fin_intervalle, salle in intervalles:
        debut_fenetre = debut + (
            (debut_intervalle - debut) // duree
        ) * duree

        while debut_fenetre < fin_intervalle:
            fin_fenetre = debut_fenetre + duree
            debut_chevauchement = max(debut_intervalle, debut_fenetre)
            fin_chevauchement = min(fin_intervalle, fin_fenetre)
            if debut_chevauchement < fin_chevauchement:
                durees_par_salle = durees_fenetres.setdefault(
                    debut_fenetre, {}
                )
                durees_par_salle[salle] = (
                    durees_par_salle.get(salle, pd.Timedelta(0))
                    + fin_chevauchement
                    - debut_chevauchement
                )
            debut_fenetre = fin_fenetre

    for debut_fenetre, fenetre in dataframe.groupby(
        pd.Grouper(freq=duree, origin=debut)
    ):
        if not fenetre.empty:
            durees_par_salle = durees_fenetres.get(debut_fenetre, {})

            salle_dominante = (
                max(durees_par_salle, key=durees_par_salle.get)
                if durees_par_salle
                else None
            )
            resultats.append(
                (
                    fenetre.index[0].value / 1_000_000_000,
                    fenetre.loc[
                        ~fenetre["capteur"].isin(
                            ["T001", "T002", "T003", "T004", "T005"]
                        ),
                        "capteur",
                    ].nunique(),
                    salle_dominante,
                    duree.total_seconds(),
                )
            )

    return resultats



# Première date disponible
debut = df.index.min()

# Durée de chaque fenêtre, en minutes
x = 30
duree = pd.Timedelta(minutes=x)

MAPPING_CAPTEURS_aruba = {
    # Chambre principale
    'M001': 'Chambre', 
    'M002': 'Chambre', 
    'M003': 'Chambre',
    'M004': 'Chambre', 
    'M005': 'Chambre', 
    'M006': 'Chambre',
    'M007': 'Chambre',
    
    'M008': 'Chambre',
    'M009': 'Chambre',
    'M010': 'Chambre',
    'M011': 'Chambre',
    'M012': 'Chambre',
    'ENTERHOME': 'Chambre',
    'LEAVEHOME': 'Chambre',

    # Salle de bain
    'M015': 'Salle_de_bain', 
    'M016': 'Salle_de_bain',
    'M017': 'Salle_de_bain',

    # Cuisine
    'M018': 'Cuisine', 
    'M019': 'Cuisine', 
    'M020': 'Cuisine',
    'M051': 'Cuisine', 
    'M052': 'Cuisine',

    # Salon / Salle à manger
    'M013': 'Salon', 
    'M014': 'Salon', 
    'M021': 'Salon',
    'M022': 'Salon', 
    'M023': 'Salon', 
    'M024': 'Salon',
    'M025': 'Salon', 
    'M026': 'Salon', 
    'M027': 'Salon',
    'M028': 'Salon', 
    'M029': 'Salon',

    # Couloirs et entrée
    'M030': 'Couloir', 
    'M031': 'Couloir',

    # Portes
    'D001': 'Porte_Entree',
    'D002': 'Porte_Arriere',
    'D004': 'Placard',

    # Température
    'T001': 'Temperature', 
    'T002': 'Temperature',
    'T003': 'Temperature', 
    'T004': 'Temperature',
    'T005': 'Temperature'
}

resultats_fenetres = informations_fenetres(df, duree)
print(
    "Timestamp Unix (s) | Nombre de capteurs différents | "
    "Pièce dominante | Durée de la fenêtre (secondes)"
)
for timestamp, nombre_capteurs, salle_dominante, duree_fenetre in resultats_fenetres:
    if salle_dominante is None:
        salle_affichee = "Indéterminée"
    else:
        salle_affichee = salle_dominante
    print(
        timestamp,
        "|",
        nombre_capteurs,
        "|",
        salle_affichee,
        "|",
        duree_fenetre,
    )