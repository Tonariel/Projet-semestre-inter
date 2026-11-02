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