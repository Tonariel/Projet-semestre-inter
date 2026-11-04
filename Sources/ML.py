import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler


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


def evaluer_modele(df_eval, colonne_verite_terrain='anomalie_reelle'):
    """
    Compare les prédictions de la baseline avec les vraies anomalies injectées.
    """

    # Extraction des colonnes pour simplifier la lecture
    y_vrai = df_eval[colonne_verite_terrain]
    y_pred = df_eval['prediction_baseline']

    # 1. Calcul des métriques statistiques standards
    # zero_division=0 évite les crashs si le modèle ne prédit aucune anomalie
    precision = precision_score(y_vrai, y_pred, zero_division=0)
    rappel = recall_score(y_vrai, y_pred, zero_division=0)
    f1 = f1_score(y_vrai, y_pred, zero_division=0)

    # 2. Extraction des Faux Positifs (fausses alertes) via la matrice de confusion
    # tn (Vrais Négatifs), fp (Faux Positifs), fn (Faux Négatifs), tp (Vrais Positifs)
    tn, fp, fn, tp = confusion_matrix(y_vrai, y_pred).ravel()

    # 3. Calcul de la métrique métier : Faux Positifs par jour
    # On calcule la durée totale du dataset évalué
    nb_jours = (df_eval['timestamp'].max() - df_eval['timestamp'].min()).days

    # Sécurité au cas où on teste sur un bout de fichier de moins de 24h
    if nb_jours == 0:
        nb_jours = 1 
        
    fp_par_jour = fp / nb_jours
    
    # 4. Affichage propre du rapport pour vos tests en console
    print("\n=== RAPPORT D'ÉVALUATION : BASELINE ===")
    print(f"Précision : {precision:.2f} (Quand l'alarme sonne, est-ce justifié ?)")
    print(f"Rappel    : {rappel:.2f} (Combien de vraies anomalies ont été détectées ?)")
    print(f"F1-Score  : {f1:.2f} (Le compromis global)")
    print("-" * 40)
    print(f"Faux Négatifs (Ratés) : {fn}")
    print(f"Faux Positifs (Total) : {fp}")
    print(f"Faux Positifs / Jour  : {fp_par_jour:.2f}")
    print("=======================================\n")
    
    return precision, rappel, f1, fp_par_jour


def executer_modele_ocsvm(df_train, df_test, colonnes_features):
    """
    Entraîne un modèle One-Class SVM sur les données normales
    et détecte les anomalies sur les données de test.
    """
    # 1. Mise à l'échelle obligatoire pour le SVM !
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(df_train[colonnes_features])
    X_test_scaled = scaler.transform(df_test[colonnes_features])

    # 2. Initialisation du One-Class SVM
    # 'nu' est l'équivalent de 'contamination' (le % d'anomalies attendu)
    modele_svm = OneClassSVM(kernel='rbf', gamma='scale', nu=0.01)

    # 3. Entraînement
    modele_svm.fit(X_train_scaled)

    # 4. Prédictions
    df_resultats = df_test.copy()
    predictions_brutes = modele_svm.predict(X_test_scaled)
    df_resultats['prediction_ml'] = np.where(predictions_brutes == -1, 1, 0)
    
    # 5. Score d'anomalie continu (inversé pour que les gros scores = anomalie)
    df_resultats['score_anomalie'] = -modele_svm.decision_function(X_test_scaled)

    return df_resultats, modele_svm