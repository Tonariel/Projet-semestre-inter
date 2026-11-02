# Classe qui représente un proche aidant
class Proche:

    def __init__(self, nom, prenom, courriel, numero):
        self.nom = nom
        self.prenom = prenom
        self.courriel = courriel
        self.numero = numero

    # Afficher les informations du proche
    def afficher(self):
        print(f"Nom : {self.nom}")
        print(f"Prénom : {self.prenom}")
        print(f"Courriel : {self.courriel}")
        print(f"Numéro : {self.numero}")


# Liste qui contient tous les proches
proches = []


# CREATE : créer un proche
def creer_proche():
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    numero = input("Numéro de téléphone : ")
    courriel = input("Courriel : ")

    # Création d'un objet Proche
    nouveau_proche = Proche(nom, prenom, courriel, numero)

    # Ajout de l'objet dans la liste
    proches.append(nouveau_proche)

    print("Proche ajouté avec succès !")


# READ : afficher les proches
def afficher_proches():

    if len(proches) == 0:
        print("Aucun proche enregistré.")
        return

    print("\n--- Liste des proches ---")

    for i, proche in enumerate(proches):
        print(f"\nProche {i + 1}")
        proche.afficher()


# UPDATE : modifier un proche
def modifier_proche():

    afficher_proches()

    if len(proches) == 0:
        return

    choix = int(input("\nQuel proche voulez-vous modifier ? ")) - 1

    if choix < 0 or choix >= len(proches):
        print("Numéro invalide.")
        return

    # Modification des attributs de l'objet
    proches[choix].nom = input("Nouveau nom : ")
    proches[choix].prenom = input("Nouveau prénom : ")
    proches[choix].numero = input("Nouveau numéro : ")

    print("Proche modifié avec succès !")


# DELETE : supprimer un proche
def supprimer_proche():

    afficher_proches()

    if len(proches) == 0:
        return

    choix = int(input("\nQuel proche voulez-vous supprimer ? ")) - 1

    if choix < 0 or choix >= len(proches):
        print("Numéro invalide.")
        return

    proches.pop(choix)

    print("Proche supprimé avec succès !")


# MENU
while True:

    print("\n===== GESTION DES PROCHES =====")
    print("1. Créer un proche")
    print("2. Afficher les proches")
    print("3. Modifier un proche")
    print("4. Supprimer un proche")
    print("5. Quitter")

    choix = input("Votre choix : ")

    if choix == "1":
        creer_proche()

    elif choix == "2":
        afficher_proches()

    elif choix == "3":
        modifier_proche()

    elif choix == "4":
        supprimer_proche()

    elif choix == "5":
        print("Au revoir !")
        break

    else:
        print("Choix invalide.")