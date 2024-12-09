import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configurations principales
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Validation des configurations critiques
if not DATABASE_URL:
    raise ValueError("DATABASE_URL n'est pas défini.")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY n'est pas défini.")
