import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix


def execute_Baseline(df):
    """
    Applique un modèle de référence basé sur des règles et l'IQR
    pour détecter les 5 scénarios d'anomalies.
    """
    df_eval = df.copy()

    df_eval['prediction_baseline'] = 0  # Initialisation de la colonne de prédiction

    # Seuil Fixe pour la détection d'anomalies

    # inactivité prolongée
    seuil_inactivite = 4 * 3600 # 4h

    # test si il fait jour ou nuit pour l'inactivité prolongée
    heure = df_eval['timestamp'].dt.hour
    est_le_jour = (heure >= 8) & (heure < 21)

    # CORRECTION 1 : Ajout des parenthèses obligatoires
    masque_inactivite = (df_eval['inactivite'] > seuil_inactivite) & est_le_jour

    # activité nocturne 
    masque_nuit = ((heure >= 2) & (heure <= 5)) & (df_eval['niveau_activite'] > 10)

    # sortie inhabituelle
    masque_sortie = ((heure >= 1) & (heure <= 5)) & (df_eval['piece_dominante'] == 'Porte_Entree')

    # détection d'anomalies basée sur l'IQR pour les autres scénarios
    masque_iqr = pd.Series(False, index=df_eval.index)

    pieces = df_eval['piece_dominante'].unique()
    for piece in pieces:
        if piece == 'Inactif':
            continue

        # CORRECTION 2 : Indentation de tout ce bloc à l'intérieur de la boucle
        donnees_piece = df_eval[df_eval['piece_dominante'] == piece]
        Q1 = donnees_piece['niveau_activite'].quantile(0.25)
        Q3 = donnees_piece['niveau_activite'].quantile(0.75)
        IQR = Q3 - Q1

        limite_haute = Q3 + 1.5 * IQR

        masque_iqr = masque_iqr | ((df_eval['piece_dominante'] == piece) & (df_eval['niveau_activite'] > limite_haute))

    # application des règles pour détecter les anomalies
    df_eval.loc[masque_inactivite | masque_nuit | masque_sortie | masque_iqr, 'prediction_baseline'] = 1
    
    return df_eval