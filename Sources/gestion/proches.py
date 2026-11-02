from DB import session, Proche

class GestionnaireProches:
    """Classe responsable de toute la logique métier et des opérations sur les proches."""
    
    def __init__(self, db_session):
        # Le gestionnaire reçoit la session de base de données à sa création
        self.session = db_session

    def creer(self):
        courriel = input("Courriel : ")
        numero = input("Numéro de téléphone : ")
        type_notif = input("Type de notification (courriel/sms) : ")
        priorite = int(input("Priorité : "))
        
        # Instanciation du modèle de données SQLAlchemy
        nouveau_proche = Proche(
            courriel=courriel, 
            numero=numero,
            type_notification=type_notif,
            priorite=priorite
        )
        
        self.session.add(nouveau_proche)
        self.session.commit()
        print("Proche ajouté avec succès !")

    def afficher_tous(self):
        proches_db = self.session.query(Proche).all()
        
        if not proches_db:
            print("Aucun proche enregistré.")
            return

        print("\n--- Liste des proches ---")
        for proche in proches_db:
            print(f"ID: {proche.id} | Courriel: {proche.courriel} | Tel: {proche.numero}")

    def supprimer(self):
        self.afficher_tous()
        choix_id = int(input("\nEntrez l'ID du proche à supprimer : "))
        
        proche = self.session.query(Proche).filter(Proche.id == choix_id).first()
        
        if proche:
            self.session.delete(proche)
            self.session.commit()
            print("Proche supprimé avec succès !")
        else:
            print("ID introuvable.")


# --- Utilisation du gestionnaire orienté objet dans le menu ---
if __name__ == "__main__":
    # On instancie l'objet gestionnaire en lui injectant la session
    gestionnaire = GestionnaireProches(session)
    
    while True:
        print("\n===== GESTION DES PROCHES =====")
        choix = input("1. Créer | 2. Afficher | 3. Supprimer | 4. Quitter : ")
        
        if choix == "1":
            gestionnaire.creer()
        elif choix == "2":
            gestionnaire.afficher_tous()
        elif choix == "3":
            gestionnaire.supprimer()
        elif choix == "4":
            print("Au revoir !")
            break