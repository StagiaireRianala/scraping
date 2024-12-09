from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import models, schemas
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Initialisation du contexte pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hache le mot de passe en utilisant bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si le mot de passe en clair correspond au mot de passe haché.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Crée un token JWT avec une date d'expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    """
    Authentifie un utilisateur en vérifiant ses identifiants.
    """
    # Recherche l'utilisateur dans la base de données
    user = db.query(models.Utilisateur).filter(models.Utilisateur.email == username).first()
    if not user:
        print("Utilisateur non trouvé : ", username)  # Log utilisateur introuvable
        return None

    # Vérifie le mot de passe
    if not verify_password(password, user.mdp):
        print("Mot de passe invalide pour : ", username)  # Log mot de passe invalide
        return None

    return user


def create_user(db: Session, user: schemas.UtilisateurCreate):
    """
    Crée un nouvel utilisateur avec un mot de passe haché.
    """
    hashed_password = get_password_hash(user.mdp)
    # Crée un objet utilisateur basé sur le modèle SQLAlchemy
    db_user = models.Utilisateur(
        name=user.name,  # Nom de l'utilisateur
        email=user.email,  # Email de l'utilisateur
        mdp=hashed_password  # Mot de passe haché
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
