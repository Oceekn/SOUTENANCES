# 🏦 My Surety + - Application d'Analyse de Risque de Crédit

## 📋 Description

Application web complète pour l'analyse et la simulation du risque de crédit utilisant les méthodes Monte Carlo et Bootstrap. L'application permet de calculer les provisions nécessaires et d'évaluer les niveaux de risque associés.

## 🚀 Fonctionnalités

- **Upload de fichiers CSV** : Support des fichiers lending et recovery
- **Simulations Monte Carlo** : Génération aléatoire basée sur la distribution de Poisson
- **Simulations Bootstrap** : Rééchantillonnage avec remise des données historiques
- **Calculs de provisions** : Estimation des provisions nécessaires
- **Analyse de risque** : Calcul bidirectionnel risque ↔ provision
- **Visualisations** : Graphiques de trajectoires et courbes de densité
- **Authentification** : Système complet avec réinitialisation de mot de passe

## 🛠️ Technologies

### Backend
- **Django 5.0.2** - Framework web Python
- **Django REST Framework** - API REST
- **Pandas** - Manipulation de données
- **NumPy** - Calculs numériques
- **SciPy** - Statistiques et distributions
- **Matplotlib/Seaborn** - Visualisations
- **Scikit-learn** - Machine learning

### Frontend
- **React 18** - Interface utilisateur
- **Ant Design** - Composants UI
- **Recharts** - Graphiques
- **Styled Components** - Styling
- **Axios** - Requêtes HTTP

## 📦 Installation

### Prérequis
- Python 3.11+
- Node.js 18+
- npm ou yarn

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd appli-nana
```

### 2. Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 3. Frontend (React)
```bash
cd frontend
npm install
npm start
```

## 🔧 Configuration

### Variables d'environnement
Créer un fichier `.env` dans le dossier backend :
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### Base de données
L'application utilise SQLite par défaut. Pour PostgreSQL ou MySQL, modifier les paramètres dans `settings.py`.

## 📊 Utilisation

1. **Connexion** : Créer un compte ou se connecter
2. **Upload** : Télécharger les fichiers CSV (lending et recovery)
3. **Configuration** : Choisir la méthode (Monte Carlo/Bootstrap) et paramètres
4. **Simulation** : Lancer la simulation
5. **Analyse** : Consulter les résultats et calculer les risques

## 📁 Structure des fichiers CSV

### Fichier Lending
```
ref_date;interval;50;100;200;250;500;1000;1500;2000;2500;5000
2023-01-01;1;10;5;2;1;0;0;0;0;0;0
```

### Fichier Recovery
```
SDATE;INTERVAL;5;34;50;61;90;100;125;173;200;215;235;250;300;435;500;600;870;1000;1080;1350;1500;1624;1917;2000;2096;2390;2500;3000;4001;5000
2023-01-01;1;2;1;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0
```

## 🔐 Authentification

- **Inscription** : Création de compte avec email
- **Connexion** : Authentification par token
- **Mot de passe oublié** : Réinitialisation par email
- **Profil** : Gestion des informations utilisateur

## 📈 API Endpoints

### Authentification
- `POST /api/users/register/` - Inscription
- `POST /api/users/login/` - Connexion
- `POST /api/users/logout/` - Déconnexion
- `GET /api/users/profile/` - Profil utilisateur

### Simulations
- `GET /api/simulations/` - Liste des simulations
- `POST /api/simulations/` - Créer une simulation
- `GET /api/simulations/{id}/status/` - Statut de simulation
- `GET /api/simulations/{id}/results/` - Résultats de simulation
- `POST /api/simulations/{id}/calculate_risk/` - Calcul de risque

## 🚀 Déploiement

### Production
1. Configurer les variables d'environnement
2. Installer les dépendances
3. Exécuter les migrations
4. Collecter les fichiers statiques
5. Configurer le serveur web (Nginx/Apache)
6. Configurer le serveur WSGI (Gunicorn/uWSGI)

### Docker (optionnel)
```bash
docker-compose up -d
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème, créer une issue sur GitHub ou contacter l'équipe de développement.

---

**Développé avec ❤️ pour l'analyse de risque de crédit**