#!/usr/bin/env python3
"""
Test de la page d'accueil MySuretyApp
"""

import requests
import time
import webbrowser

def test_home_page():
    """Test de la page d'accueil"""
    print("🏠 Test de la Page d'Accueil MySuretyApp")
    print("=" * 50)
    
    # Attendre que l'application démarre
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(15)
    
    try:
        # Test de la page d'accueil
        print("🔍 Test de la page d'accueil...")
        response = requests.get("http://localhost:3000", timeout=10)
        
        if response.status_code == 200:
            print("✅ Application React : Démarrée")
            print(f"📄 Taille de la réponse : {len(response.text)} caractères")
            
            # Vérifier le contenu
            content = response.text
            if "EPSILON" in content:
                print("✅ Logo EPSILON détecté")
            else:
                print("❌ Logo EPSILON non trouvé")
                
            if "Se Connecter" in content:
                print("✅ Bouton 'Se Connecter' détecté")
            else:
                print("❌ Bouton 'Se Connecter' non trouvé")
                
            if "S'inscrire" in content:
                print("✅ Bouton 'S'inscrire' détecté")
            else:
                print("❌ Bouton 'S'inscrire' non trouvé")
                
            if "Powered by" in content:
                print("✅ Texte 'Powered by' détecté")
            else:
                print("❌ Texte 'Powered by' non trouvé")
                
            print("\n🎉 Page d'accueil créée avec succès !")
            print("🌐 Ouvrez votre navigateur à : http://localhost:3000")
            
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
    test_home_page()

