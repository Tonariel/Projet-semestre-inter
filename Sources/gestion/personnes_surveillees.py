from DB import Utilisateur, PersonneSurveillee, RoleUtilisateur

class GestionnairePersonnesSurveillees:
    def __init__(self, db_session):
        self.session = db_session

    def creer(self):
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        
        # 1. Créer l'utilisateur générique
        nouvel_utilisateur = Utilisateur(nom=nom, prenom=prenom, role=RoleUtilisateur.PERSONNE_SURVEILLEE)
        self.session.add(nouvel_utilisateur)
        self.session.commit()
        
        # 2. Lier cet utilisateur à la table PersonneSurveillee
        nouvelle_personne = PersonneSurveillee(utilisateur_id=nouvel_utilisateur.id)
        self.session.add(nouvelle_personne)
        self.session.commit()
        print("Personne surveillée créée !")

    def afficher(self):
        personnes = self.session.query(PersonneSurveillee).all()
        if not personnes:
            print("Aucune personne surveillée.")
            return
            
        for p in personnes:
            print(f"ID Personne: {p.id} | ID Utilisateur: {p.utilisateur_id}")

    def modifier(self):
        personnes = self.session.query(PersonneSurveillee).all()
        if not personnes:
            print("Aucune personne surveillée.")
            return

        self.afficher()
        try:
            choix_id = int(input("\nEntrez l'ID de la personne surveillée à modifier : "))
        except ValueError:
            print("Erreur : Veuillez entrer un numéro valide.")
            return

        personne = self.session.query(PersonneSurveillee).filter(
            PersonneSurveillee.id == choix_id
        ).first()

        if not personne:
            print("ID introuvable dans la base de données.")
            return

        utilisateur = self.session.query(Utilisateur).filter(
            Utilisateur.id == personne.utilisateur_id,
            Utilisateur.role == RoleUtilisateur.PERSONNE_SURVEILLEE
        ).first()
        if not utilisateur:
            print("Utilisateur associé introuvable.")
            return

        print(f"\n--- Modification de la personne surveillée #{personne.id} ---")
        print("(Appuyez sur Entrée sans rien écrire pour conserver la valeur actuelle)")

        nouveau_nom = input(f"Nom [{utilisateur.nom}] : ")
        if nouveau_nom:
            utilisateur.nom = nouveau_nom

        nouveau_prenom = input(f"Prénom [{utilisateur.prenom}] : ")
        if nouveau_prenom:
            utilisateur.prenom = nouveau_prenom

        self.session.commit()
        print("Personne surveillée modifiée avec succès !")

    def supprimer(self):
        personnes = self.session.query(PersonneSurveillee).all()
        if not personnes:
            print("Aucune personne surveillée.")
            return

        self.afficher()
        choix_id = int(input("\nEntrez l'ID de la personne surveillée à supprimer : "))

        personne = self.session.query(PersonneSurveillee).filter(
            PersonneSurveillee.id == choix_id
        ).first()

        if personne:
            utilisateur = self.session.query(Utilisateur).filter(
                Utilisateur.id == personne.utilisateur_id
            ).first()

            self.session.delete(personne)
            if utilisateur:
                self.session.delete(utilisateur)
            self.session.commit()
            print("Personne surveillée supprimée avec succès !")
        else:
            print("ID introuvable.")