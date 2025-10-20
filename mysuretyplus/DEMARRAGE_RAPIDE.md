# 🚀 DÉMARRAGE RAPIDE - APPLICATION D'ANALYSE DE RISQUE DE CRÉDIT

## ⚡ **DÉMARRAGE EN 3 ÉTAPES**

### **Étape 1 : Lancer l'Application**
```bash
# Windows (double-clic)
start.bat

# Ou manuellement
cd backend && python manage.py runserver
cd frontend && npm start
```

### **Étape 2 : Accéder à l'Application**
- **Interface utilisateur** : http://localhost:3000
- **API backend** : http://localhost:8000/api/
- **Admin** : http://localhost:8000/admin/

### **Étape 3 : Se Connecter**
```
Username : testuser
Password : testpass123
```

## 📁 **PREMIÈRE UTILISATION**

### **1. Upload de Fichiers CSV**
- **Lending** : Fichier des emprunts (format requis)
- **Recovery** : Fichier des remboursements (format requis)

### **2. Configuration Simulation**
- **Méthode** : Monte Carlo (rapide) ou Bootstrap (précis)
- **Échantillons** : 100 pour test, 1000+ pour production
- **Confiance** : 0.95 (95%) recommandé

### **3. Lancement et Résultats**
- Cliquez "Lancer la Simulation"
- Surveillez la progression
- Analysez les graphiques et métriques

## 🔧 **EN CAS DE PROBLÈME**

### **Problème de Démarrage**
```bash
# Vérifier Python
python --version

# Vérifier Node.js
node --version

# Réinstaller les dépendances
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

### **Problème de Port**
- **Port 8000 occupé** : Changez le port Django
- **Port 3000 occupé** : Changez le port React

### **Problème de Base de Données**
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 📊 **FORMAT CSV REQUIS**

```csv
ref_date;interval;SDATE;INTERVAL;50;100;500;1000
2024-01-01;1;2024-01-01;1;5;3;2;1
2024-01-02;2;2024-01-02;2;3;4;1;2
```

**Colonnes obligatoires** : ref_date, interval, SDATE, INTERVAL
**Colonnes numériques** : Dénominations (50, 100, 500, 1000, etc.)

## 🎯 **FONCTIONNALITÉS PRINCIPALES**

- ✅ **Upload et validation CSV**
- ✅ **Simulations Monte Carlo/Bootstrap**
- ✅ **Graphiques interactifs**
- ✅ **Calculs de provision**
- ✅ **Métriques de risque**
- ✅ **Calculateur bidirectionnel**

## 📞 **AIDE RAPIDE**

- **Guide complet** : `GUIDE_UTILISATION.md`
- **Tests** : `python test_complet.py`
- **Tests composants** : `python test_components.py`
- **Logs** : Console Django + Console navigateur (F12)

---

## 🎉 **VOUS ÊTES PRÊT !**

Votre application d'analyse de risque de crédit est maintenant opérationnelle !

**Bonne analyse !** 🚀


