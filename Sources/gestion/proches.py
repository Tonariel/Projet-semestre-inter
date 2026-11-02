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

    def modifier(self):
        # 1. Afficher la liste pour voir les ID disponibles
        self.afficher()
        
        # S'il n'y a personne, on arrête la fonction ici
        if self.session.query(Proche).count() == 0:
            return

        # 2. Demander l'ID de manière sécurisée (évite que le programme plante si on tape une lettre)
        try:
            choix_id = int(input("\nEntrez l'ID du proche à modifier : "))
        except ValueError:
            print("Erreur : Veuillez entrer un numéro valide.")
            return

        # 3. Chercher l'objet dans la base de données
        proche = self.session.query(Proche).filter(Proche.id == choix_id).first()
        
        if not proche:
            print("ID introuvable dans la base de données.")
            return

        print(f"\n--- Modification du proche #{proche.id} ---")
        print("(Appuyez sur Entrée sans rien écrire pour conserver la valeur actuelle)")

        # 4. Mise à jour des champs avec conservation de l'ancienne valeur si l'entrée est vide
        nouveau_courriel = input(f"Courriel [{proche.courriel}] : ")
        if nouveau_courriel:
            proche.courriel = nouveau_courriel

        nouveau_numero = input(f"Numéro [{proche.numero}] : ")
        if nouveau_numero:
            proche.numero = nouveau_numero

        nouveau_type = input(f"Type notification [{proche.type_notification}] : ")
        if nouveau_type:
            proche.type_notification = nouveau_type

        nouvelle_priorite = input(f"Priorité [{proche.priorite}] : ")
        if nouvelle_priorite:
            try:
                proche.priorite = int(nouvelle_priorite)
            except ValueError:
                print("Priorité invalide ignorée. L'ancienne priorité est conservée.")

        # 5. Validation de la transaction
        self.session.commit()
        print("Proche modifié avec succès !")

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