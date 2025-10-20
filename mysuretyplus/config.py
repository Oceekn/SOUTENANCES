# Configuration de l'application Nana
# Ce fichier contient les paramètres de configuration par défaut

import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"

# Configuration Django
DJANGO_SETTINGS = {
    "DEBUG": True,
    "SECRET_KEY": "django-insecure-change-this-in-production",
    "ALLOWED_HOSTS": ["localhost", "127.0.0.1"],
    "DATABASE": "sqlite:///db.sqlite3",
    "CORS_ALLOW_ALL_ORIGINS": True,
    "CORS_ALLOW_CREDENTIALS": True,
    "MEDIA_URL": "/media/",
    "MEDIA_ROOT": str(BACKEND_DIR / "media"),
    "STATIC_URL": "/static/",
    "STATIC_ROOT": str(BACKEND_DIR / "staticfiles"),
}

# Configuration des ports
PORTS = {
    "DJANGO": 8000,
    "REACT": 3000,
}

# Configuration des simulations
SIMULATION_CONFIG = {
    "MAX_SAMPLES": 15000,
    "DEFAULT_SAMPLES": 1000,
    "MIN_SAMPLES": 10,
    "DEFAULT_ALPHA": 0.95,
    "SUPPORTED_METHODS": ["montecarlo", "bootstrap"],
}

# Configuration des fichiers
FILE_CONFIG = {
    "MAX_SIZE": 50 * 1024 * 1024,  # 50MB
    "ALLOWED_EXTENSIONS": [".csv"],
    "ENCODING": "utf-8",
    "DELIMITER": ";",
}

# Configuration des logs
LOG_CONFIG = {
    "LEVEL": "INFO",
    "FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "FILE": str(BACKEND_DIR / "logs" / "app.log"),
}

# Configuration des performances
PERFORMANCE_CONFIG = {
    "CHUNK_SIZE": 1000,
    "TIMEOUT": 300,  # 5 minutes
    "MAX_WORKERS": 4,
}

# Configuration de sécurité
SECURITY_CONFIG = {
    "SESSION_COOKIE_SECURE": False,
    "CSRF_COOKIE_SECURE": False,
    "SECURE_SSL_REDIRECT": False,
    "PASSWORD_MIN_LENGTH": 8,
    "TOKEN_EXPIRY": 24 * 60 * 60,  # 24 heures
}

def get_django_settings():
    """Retourne les paramètres Django formatés"""
    return DJANGO_SETTINGS

def get_simulation_config():
    """Retourne la configuration des simulations"""
    return SIMULATION_CONFIG

def get_file_config():
    """Retourne la configuration des fichiers"""
    return FILE_CONFIG

def get_ports():
    """Retourne la configuration des ports"""
    return PORTS

def create_directories():
    """Crée les répertoires nécessaires"""
    directories = [
        BACKEND_DIR / "media",
        BACKEND_DIR / "staticfiles",
        BACKEND_DIR / "logs",
        FRONTEND_DIR / "build",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Répertoire créé: {directory}")

if __name__ == "__main__":
    print("Configuration de l'Application Nana")
    print("=" * 40)
    print(f"Répertoire de base: {BASE_DIR}")
    print(f"Backend: {BACKEND_DIR}")
    print(f"Frontend: {FRONTEND_DIR}")
    print(f"Port Django: {PORTS['DJANGO']}")
    print(f"Port React: {PORTS['REACT']}")
    print()
    
    # Créer les répertoires
    create_directories()
    
    print("\nConfiguration terminée!")
