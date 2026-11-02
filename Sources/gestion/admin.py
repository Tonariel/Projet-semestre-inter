from DB import Utilisateur, RoleUtilisateur

class GestionnaireAdmin:
    def __init__(self, db_session):
        self.session = db_session

    def creer(self):
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        
        nouvel_admin = Utilisateur(nom=nom, prenom=prenom, role=RoleUtilisateur.ADMINISTRATEUR)
        self.session.add(nouvel_admin)
        self.session.commit()
        print("Administrateur créé !")

    def afficher(self):
        admins = self.session.query(Utilisateur).filter(Utilisateur.role == RoleUtilisateur.ADMINISTRATEUR).all()
        if not admins:
            print("Aucun administrateur.")
            return
        
        for admin in admins:
            print(f"ID: {admin.id} | {admin.prenom} {admin.nom}")

    def modifier(self):
        admins = self.session.query(Utilisateur).filter(
            Utilisateur.role == RoleUtilisateur.ADMINISTRATEUR
        ).all()
        if not admins:
            print("Aucun administrateur.")
            return

        self.afficher()
        try:
            choix_id = int(input("\nEntrez l'ID de l'administrateur à modifier : "))
        except ValueError:
            print("Erreur : Veuillez entrer un numéro valide.")
            return

        admin = self.session.query(Utilisateur).filter(
            Utilisateur.id == choix_id,
            Utilisateur.role == RoleUtilisateur.ADMINISTRATEUR
        ).first()

        if not admin:
            print("ID introuvable dans la base de données.")
            return

        print(f"\n--- Modification de l'administrateur #{admin.id} ---")
        print("(Appuyez sur Entrée sans rien écrire pour conserver la valeur actuelle)")

        nouveau_nom = input(f"Nom [{admin.nom}] : ")
        if nouveau_nom:
            admin.nom = nouveau_nom

        nouveau_prenom = input(f"Prénom [{admin.prenom}] : ")
        if nouveau_prenom:
            admin.prenom = nouveau_prenom

        self.session.commit()
        print("Administrateur modifié avec succès !")

    def supprimer(self):
        admins = self.session.query(Utilisateur).filter(
            Utilisateur.role == RoleUtilisateur.ADMINISTRATEUR
        ).all()
        if not admins:
            print("Aucun administrateur.")
            return

        self.afficher()
        choix_id = int(input("\nEntrez l'ID de l'administrateur à supprimer : "))

        admin = self.session.query(Utilisateur).filter(
            Utilisateur.id == choix_id,
            Utilisateur.role == RoleUtilisateur.ADMINISTRATEUR
        ).first()

        if admin:
            self.session.delete(admin)
            self.session.commit()
            print("Administrateur supprimé avec succès !")
        else:
            print("ID introuvable.")