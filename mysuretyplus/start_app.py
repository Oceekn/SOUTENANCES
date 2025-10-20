#!/usr/bin/env python3
"""
Script de démarrage pour l'application de gestion des risques de crédit
Lance automatiquement le backend Django et le frontend React
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class AppLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
        # Chemins des projets
        self.backend_path = Path("backend")
        self.frontend_path = Path("frontend")
        
        # Vérification des chemins
        if not self.backend_path.exists():
            print("❌ Erreur: Le dossier 'backend' n'existe pas")
            sys.exit(1)
            
        if not self.frontend_path.exists():
            print("❌ Erreur: Le dossier 'frontend' n'existe pas")
            sys.exit(1)
    
    def check_dependencies(self):
        """Vérifie que toutes les dépendances sont installées"""
        print("🔍 Vérification des dépendances...")
        
        # Vérification backend
        backend_requirements = self.backend_path / "requirements.txt"
        if not backend_requirements.exists():
            print("❌ Erreur: requirements.txt manquant dans le dossier backend")
            return False
        
        # Vérification frontend
        frontend_package = self.frontend_path / "package.json"
        if not frontend_package.exists():
            print("❌ Erreur: package.json manquant dans le dossier frontend")
            return False
        
        print("✅ Dépendances trouvées")
        return True
    
    def install_dependencies(self):
        """Installe les dépendances si nécessaire"""
        print("📦 Installation des dépendances...")
        
        # Installation backend
        print("🔧 Installation des dépendances Python...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", 
                str(self.backend_path / "requirements.txt")
            ], check=True, cwd=self.backend_path)
            print("✅ Dépendances Python installées")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation des dépendances Python: {e}")
            return False
        
        # Installation frontend
        print("🔧 Installation des dépendances Node.js...")
        try:
            subprocess.run(["npm", "install"], check=True, cwd=self.frontend_path)
            print("✅ Dépendances Node.js installées")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation des dépendances Node.js: {e}")
            return False
        
        return True
    
    def setup_database(self):
        """Configure la base de données Django"""
        print("🗄️ Configuration de la base de données...")
        
        try:
            # Migrations
            subprocess.run([
                sys.executable, "manage.py", "makemigrations"
            ], check=True, cwd=self.backend_path)
            
            subprocess.run([
                sys.executable, "manage.py", "migrate"
            ], check=True, cwd=self.backend_path)
            
            # Création d'un superuser si nécessaire
            print("👤 Création d'un superuser (admin/admin)...")
            subprocess.run([
                sys.executable, "manage.py", "createsuperuser", 
                "--noinput", "--username", "admin", "--email", "admin@example.com"
            ], check=True, cwd=self.backend_path, input=b"admin\nadmin\n", stderr=subprocess.DEVNULL)
            
            print("✅ Base de données configurée")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de la configuration de la base de données: {e}")
            return False
    
    def start_backend(self):
        """Démarre le serveur Django"""
        print("🚀 Démarrage du backend Django...")
        
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, "manage.py", "runserver", "0.0.0.0:8000"
            ], cwd=self.backend_path)
            
            # Attendre que le serveur soit prêt
            time.sleep(3)
            if self.backend_process.poll() is None:
                print("✅ Backend Django démarré sur http://localhost:8000")
                return True
            else:
                print("❌ Erreur lors du démarrage du backend")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du démarrage du backend: {e}")
            return False
    
    def start_frontend(self):
        """Démarre le serveur React"""
        print("🚀 Démarrage du frontend React...")
        
        try:
            self.frontend_process = subprocess.Popen([
                "npm", "start"
            ], cwd=self.frontend_path)
            
            # Attendre que le serveur soit prêt
            time.sleep(5)
            if self.frontend_process.poll() is None:
                print("✅ Frontend React démarré sur http://localhost:3000")
                return True
            else:
                print("❌ Erreur lors du démarrage du frontend")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du démarrage du frontend: {e}")
            return False
    
    def signal_handler(self, signum, frame):
        """Gère l'arrêt propre de l'application"""
        print("\n🛑 Arrêt de l'application...")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend arrêté")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print("✅ Frontend arrêté")
        
        sys.exit(0)
    
    def monitor_processes(self):
        """Surveille les processus en arrière-plan"""
        while self.running:
            time.sleep(2)
            
            # Vérification backend
            if self.backend_process and self.backend_process.poll() is not None:
                print("❌ Le backend s'est arrêté inopinément")
                self.running = False
                break
            
            # Vérification frontend
            if self.frontend_process and self.frontend_process.poll() is not None:
                print("❌ Le frontend s'est arrêté inopinément")
                self.running = False
                break
    
    def run(self):
        """Lance l'application complète"""
        print("🎯 Lancement de l'application de gestion des risques de crédit")
        print("=" * 60)
        
        # Configuration des signaux
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Vérification et installation des dépendances
        if not self.check_dependencies():
            print("❌ Impossible de continuer sans les dépendances")
            sys.exit(1)
        
        # Installation des dépendances
        if not self.install_dependencies():
            print("❌ Impossible d'installer les dépendances")
            sys.exit(1)
        
        # Configuration de la base de données
        if not self.setup_database():
            print("❌ Impossible de configurer la base de données")
            sys.exit(1)
        
        # Démarrage des services
        if not self.start_backend():
            print("❌ Impossible de démarrer le backend")
            sys.exit(1)
        
        if not self.start_frontend():
            print("❌ Impossible de démarrer le frontend")
            sys.exit(1)
        
        print("\n🎉 Application démarrée avec succès!")
        print("📱 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000")
        print("👤 Connexion: admin / admin")
        print("\n💡 Appuyez sur Ctrl+C pour arrêter l'application")
        print("=" * 60)
        
        # Surveillance des processus
        self.monitor_processes()

def main():
    """Point d'entrée principal"""
    try:
        launcher = AppLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()





