from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

# Importation des outils pour gérer les sessions et lier les classes Python aux tables SQL
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///maison_intelligente.db', echo=True)

# Création de la classe de base dont toutes vos tables vont hériter
Base = declarative_base()


class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    role = Column(String) # "personne surveillée", "proche aidant", ou "administrateur"



class Proche(Base):
    __tablename__ = 'proches'
    
    id = Column(Integer, primary_key=True)
    numero = Column(String)
    personne_surveillee_id = relationship("Utilisateur") # ID de la personne surveillée associée
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))  # ID de l'utilisateur associé


class PersonneSurveillee(Base):
    __tablename__ = 'personnes_surveillees'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    numero = Column(String)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))  # ID de l'utilisateur associé
    Proches_ids = relationship("Proche", backref="personne_surveillee")  # Liste des proches associés

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()