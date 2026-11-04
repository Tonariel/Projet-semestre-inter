import matplotlib.pyplot as plt
import seaborn as sns

def visualiser_distribution_scores(df_resultats, colonne_verite='anomalie_reelle'):
    """
    Génère le graphique de distribution des scores d'anomalie demandé en Semaine 8.
    """
    plt.figure(figsize=(10, 6))
    
    # On trace les deux courbes de distribution superposées
    sns.histplot(data=df_resultats, x='score_anomalie', hue=colonne_verite, 
                 kde=True, bins=50, palette={0: 'blue', 1: 'red'})
    
    plt.title("Distribution des scores d'anomalie (0: Normal, 1: Anormal)")
    plt.xlabel("Score d'anomalie (plus c'est grand, plus c'est anormal)")
    plt.ylabel("Nombre d'événements")
    plt.grid(True, alpha=0.3)
    plt.show()