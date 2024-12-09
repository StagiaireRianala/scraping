from fastapi import FastAPI

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas, auth, database
from fastapi.middleware.cors import CORSMiddleware

# Créer une instance de FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, bam!"}

# Configuration du CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Route pour l'enregistrement d'un utilisateur
@app.post("/register", response_model=schemas.UtilisateurOut)
async def register_user(user: schemas.UtilisateurCreate, db: Session = Depends(database.get_db)):
    """
    Enregistre un nouvel utilisateur après avoir vérifié que le nom d'utilisateur n'est pas déjà pris.
    """
    # Vérifie si le nom d'utilisateur existe déjà
    db_user = db.query(models.Utilisateur).filter(models.Utilisateur.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Crée un nouvel utilisateur et retourne ses informations (id, username)
    return auth.create_user(db, user)

# Route pour le login d'un utilisateur
@app.post("/login", response_model=schemas.Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Authentifie un utilisateur et génère un token JWT si les informations sont valides.
    """
    print("Tentative de connexion pour :", form_data.username)  # Log des données reçues

    # Authentifie l'utilisateur
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        print("Authentification échouée pour :", form_data.username)  # Log échec
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    # Crée un token JWT
    access_token = auth.create_access_token(data={"sub": user.email})
    print("Connexion réussie pour :", user.email)  # Log succès
    return {"access_token": access_token, "token_type": "bearer"}



from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

# Définir le secret et la clé d'algorithme
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Fonction pour vérifier le token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Retourne les informations contenues dans le token
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
        )

# Route protégée pour valider l'utilisateur avec le token
@app.get("/protected")
async def get_protected_data(user: dict = Depends(verify_token)):
    return {"name": user["sub"]}  # Retourne le nom ou d'autres données de l'utilisateur

