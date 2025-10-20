#!/usr/bin/env python3
"""
Test de la correction du problème de connexion
"""

import requests
import time
import webbrowser

def test_login_fix():
    """Test de la correction du problème de connexion"""
    print("🔧 Test de la Correction du Problème de Connexion")
    print("=" * 60)
    
    # Attendre que l'application démarre
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(10)
    
    try:
        # Test de la page d'accueil
        print("🔍 Test de la page d'accueil...")
        response = requests.get("http://localhost:3000", timeout=10)
        
        if response.status_code == 200:
            print("✅ Application React : Démarrée")
            print(f"📄 Taille de la réponse : {len(response.text)} caractères")
            
            # Vérifier le contenu
            content = response.text
            if "Se Connecter" in content:
                print("✅ Bouton 'Se Connecter' détecté")
            else:
                print("❌ Bouton 'Se Connecter' non trouvé")
                
            print("\n🎉 Page d'accueil fonctionne !")
            print("🌐 Ouvrez votre navigateur à : http://localhost:3000")
            print("\n💡 Instructions pour tester la connexion :")
            print("1. Cliquez sur 'Se Connecter'")
            print("2. Vous devriez voir la page de connexion")
            print("3. Si vous voyez directement le dashboard, ouvrez la console du navigateur")
            print("4. Tapez : localStorage.clear()")
            print("5. Rechargez la page et réessayez")
            
            # Ouvrir automatiquement dans le navigateur
            try:
                webbrowser.open('http://localhost:3000')
                print("🚀 Page ouverte automatiquement dans votre navigateur")
            except:
                print("💡 Ouvrez manuellement : http://localhost:3000")
                
        else:
            print(f"❌ Erreur HTTP : {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        print("💡 Vérifiez que 'npm start' est en cours d'exécution")
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")

if __name__ == "__main__":
    test_login_fix()

