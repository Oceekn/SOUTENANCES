# 🚀 Guide de Démarrage Rapide - Application Nana

## 📋 Prérequis

- **Python 3.7+** installé et dans le PATH
- **Node.js 14+** installé et dans le PATH
- **npm** (inclus avec Node.js)

## 🎯 Démarrage Automatique

### Windows
1. Double-cliquez sur `start.bat`
2. Laissez les fenêtres s'ouvrir automatiquement
3. L'application s'ouvrira dans votre navigateur

### Linux/Mac
1. Ouvrez un terminal
2. Rendez le script exécutable : `chmod +x start.sh`
3. Exécutez : `./start.sh`

### PowerShell (Windows)
1. Ouvrez PowerShell en tant qu'administrateur
2. Exécutez : `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Exécutez : `.\start.ps1`

## 🔧 Démarrage Manuel

### Backend Django
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py runserver
```

### Frontend React
```bash
cd frontend
npm install
npm start
```

## 🧪 Test de Configuration

Exécutez le script de test pour vérifier que tout est correctement configuré :

```bash
python test_setup.py
```

## 📊 Utilisation de l'Application

### 1. Créer un compte
- Accédez à `http://localhost:3000`
- Cliquez sur "S'inscrire"
- Remplissez le formulaire

### 2. Se connecter
- Utilisez vos identifiants
- Vous accédez au tableau de bord

### 3. Charger des données
- Téléchargez votre fichier `lending.csv` (emprunts)
- Téléchargez votre fichier `recovery.csv` (remboursements)
- Format attendu : colonnes avec dénominations (50, 100, 200, etc.)

### 4. Configurer la simulation
- Choisissez la méthode : Monte Carlo ou Bootstrap
- Définissez le nombre d'échantillons (10 à 1000 pour les tests)
- Choisissez le niveau de confiance (alpha)

### 5. Lancer la simulation
- Cliquez sur "Lancer la simulation"
- Suivez le progrès en temps réel
- Visualisez les résultats

### 6. Analyser les résultats
- **Graphique de trajectoire** : ligne réelle + faisceau simulé
- **Courbe de densité** : distribution des provisions avec zones de risque
- **Calculateur bidirectionnel** : risque ↔ provision

## 📁 Structure des Fichiers CSV

### Format Lending (Emprunts)
```csv
ref_date;INTERVAL;50;100;200;500;1000;2000;5000
2024-01-01;09:00;5;3;2;1;0;0;0
```

### Format Recovery (Remboursements)
```csv
ref_date;INTERVAL;50;100;200;500;1000;2000;5000
2024-01-01;09:00;2;1;1;0;0;0;0
```

**Explication :**
- `ref_date` : Date de référence
- `INTERVAL` : Heure de la transaction
- Colonnes numériques : Nombre de transactions par dénomination
- Calcul : 50×5 + 100×3 + 200×2 + 500×1 = 250 + 300 + 400 + 500 = 1450

## 🚨 Dépannage

### Erreur "Python non trouvé"
- Vérifiez que Python est installé et dans le PATH
- Redémarrez votre terminal

### Erreur "Node.js non trouvé"
- Vérifiez que Node.js est installé et dans le PATH
- Redémarrez votre terminal

### Erreur de port déjà utilisé
- Arrêtez les processus sur les ports 8000 et 3000
- Ou modifiez les ports dans `config.py`

### Erreur de dépendances
- Exécutez `pip install -r backend/requirements.txt`
- Exécutez `npm install` dans le dossier frontend

### Erreur de base de données
- Supprimez `backend/db.sqlite3` si il existe
- Exécutez `python manage.py migrate`

## 📞 Support

- Vérifiez d'abord avec `python test_setup.py`
- Consultez les logs dans `backend/logs/` et `frontend/`
- Vérifiez la console du navigateur (F12)

## 🎉 Félicitations !

Votre application d'évaluation des risques de crédit est maintenant opérationnelle !

**URLs :**
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000
- Admin Django : http://localhost:8000/admin

**Prochaines étapes :**
1. Testez avec les fichiers d'exemple dans `sample_data/`
2. Explorez les différentes méthodes de simulation
3. Ajustez les paramètres selon vos besoins
4. Consultez le README.md pour plus de détails





