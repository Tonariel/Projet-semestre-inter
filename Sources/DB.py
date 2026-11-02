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


class Administrateur(Base):
    __tablename__ = 'administrateurs'
    
    id = Column(Integer, primary_key=True)

    
    courriel = Column(String, unique=True, nullable=False)
    
    # Lien physique vers les informations communes (nom, prénom, rôle)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))


class Proche(Base):
    __tablename__ = 'proches'
    
    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))  # ID de l'utilisateur associé
    personne_surveillee_id = Column(Integer, ForeignKey('personnes_surveillees.id')) # ID de la personne surveillée associée
    personne_surveillee = relationship("PersonneSurveillee", back_populates="proches")
    
    
    courriel = Column(String, nullable=False)
    numero = Column(String)
    type_notification = Column(String)
    priorite = Column(Integer) # Indique l'ordre de contact (ex: 1 pour principal, 2 pour secondaire)

    
    
class PersonneSurveillee(Base):
    __tablename__ = 'personnes_surveillees'
    
    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))  # ID de l'utilisateur associé
    proches = relationship("Proche", back_populates="personne_surveillee")

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()