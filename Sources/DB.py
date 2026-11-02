import enum
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum

# Importation des outils pour gérer les sessions et lier les classes Python aux tables SQL
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///maison_intelligente.db', echo=True)

# Création de la classe de base dont toutes vos tables vont hériter
Base = declarative_base()

class RoleUtilisateur(enum.Enum):
    PERSONNE_SURVEILLEE = "personne surveillée"
    PROCHE_AIDANT = "proche aidant"
    ADMINISTRATEUR = "administrateur"


class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    role = Column(Enum(RoleUtilisateur), nullable=False, default=RoleUtilisateur.PERSONNE_SURVEILLEE)


class Proche(Base):
    __tablename__ = 'proches'
    
    id = Column(Integer, primary_key=True)
    numero = Column(String)
    personne_surveillee_id = relationship("Utilisateur") # ID de la personne surveillée associée
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))  # ID de l'utilisateur associé


class PersonneSurveillee(Base):
    __tablename__ = 'personnes_surveillees'
    
    id = Column(Integer, primary_key=True)
    numero = Column(String)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))  # ID de l'utilisateur associé
    Proches_ids = relationship("Proche", backref="personne_surveillee")  # Liste des proches associés

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()