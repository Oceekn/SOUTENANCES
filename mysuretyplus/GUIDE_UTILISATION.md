# 📚 GUIDE D'UTILISATION COMPLET - APPLICATION D'ANALYSE DE RISQUE DE CRÉDIT

## 🚀 **DÉMARRAGE RAPIDE**

### **1. Lancer l'Application**
```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# Ou manuellement
cd backend && python manage.py runserver
cd frontend && npm start
```

### **2. Accès à l'Application**
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000/api/
- **Admin Django** : http://localhost:8000/admin/

### **3. Compte de Test**
```
Username : testuser
Password : testpass123
```

## 📁 **FORMAT DES FICHIERS CSV**

### **Structure Requise**
Vos fichiers CSV doivent avoir cette structure exacte :

```csv
ref_date;interval;SDATE;INTERVAL;50;100;500;1000
2024-01-01;1;2024-01-01;1;5;3;2;1
2024-01-02;2;2024-01-02;2;3;4;1;2
2024-01-03;3;2024-01-03;3;2;5;3;1
```

### **Colonnes Obligatoires**
- `ref_date` : Date de référence
- `interval` : Intervalle temporel
- `SDATE` : Date formatée
- `INTERVAL` : Intervalle formaté
- **Colonnes numériques** : Dénominations (50, 100, 500, 1000, etc.)

### **Règles de Format**
- **Séparateur** : Point-virgule (;)
- **Encodage** : UTF-8 recommandé
- **Taille max** : 10MB par fichier
- **Extension** : .csv obligatoire

## 🎯 **UTILISATION DE L'APPLICATION**

### **Étape 1 : Connexion**
1. Ouvrez http://localhost:3000
2. Cliquez sur "S'inscrire" ou "Se connecter"
3. Utilisez le compte de test ou créez le vôtre

### **Étape 2 : Upload des Fichiers**
1. **Fichier Lending** : Upload du fichier des emprunts
2. **Fichier Recovery** : Upload du fichier des remboursements
3. Vérifiez que les deux fichiers sont validés (✓ vert)

### **Étape 3 : Configuration de la Simulation**
1. **Méthode** : 
   - 🎲 **Monte Carlo** : Génération aléatoire (Poisson)
   - 🔄 **Bootstrap** : Rééchantillonnage avec remise
2. **Nombre d'échantillons** : 10 à 15,000
3. **Niveau de confiance** : 0.5 à 0.999 (ex: 0.95 = 95%)

### **Étape 4 : Lancement de la Simulation**
1. Cliquez sur "Lancer la Simulation"
2. Surveillez la progression en temps réel
3. Attendez la completion (statut "Terminé")

### **Étape 5 : Analyse des Résultats**
1. **Graphique de Trajectoire** : Ligne bleue (réel) + faisceau gris (simulations)
2. **Courbe de Densité** : Distribution des provisions avec zones de risque
3. **Métriques** : Percentiles, intervalles de confiance
4. **Calculateur de Risque** : Bidirectionnel (risque ↔ provision)

## 📊 **INTERPRÉTATION DES RÉSULTATS**

### **Provision Réelle**
- Montant calculé à partir de vos données historiques
- Basé sur le maximum du solde cumulé (lending - recovery)

### **Zones de Risque**
- **Zone 5%** (Vert clair) : Risque modéré
- **Zone 2.5%** (Vert moyen) : Risque élevé
- **Zone 1%** (Vert foncé) : Risque très élevé
- **Zone Critique** (Rouge) : Risque extrême

### **Méthodes de Simulation**
- **Monte Carlo** : Plus rapide, bon pour grandes quantités
- **Bootstrap** : Plus précis, basé sur vos données réelles

## 🔧 **FONCTIONNALITÉS AVANCÉES**

### **Calculateur de Risque Bidirectionnel**
1. **Risque → Provision** : Entrez un niveau de risque (ex: 5%) → Obtenez la provision
2. **Provision → Risque** : Entrez une provision → Obtenez le niveau de risque

### **Relancement de Simulation**
- Modifiez les paramètres
- Relancez avec les mêmes fichiers
- Comparez les résultats

### **Export des Données**
- Téléchargez les résultats
- Sauvegardez les graphiques
- Exportez les métriques

## ⚠️ **DÉPANNAGE**

### **Problèmes Courants**

#### **1. Fichiers CSV Non Validés**
- Vérifiez le format (séparateur ;)
- Vérifiez les colonnes obligatoires
- Vérifiez l'encodage (UTF-8)

#### **2. Simulation Qui Échoue**
- Réduisez le nombre d'échantillons
- Vérifiez la qualité des données
- Relancez la simulation

#### **3. Erreur d'Authentification**
- Vérifiez votre token
- Reconnectez-vous
- Vérifiez la session

#### **4. Performance Lente**
- Utilisez moins d'échantillons pour les tests
- Monte Carlo est plus rapide que Bootstrap
- Fermez d'autres applications

### **Logs et Debug**
- **Backend** : Vérifiez la console Django
- **Frontend** : Vérifiez la console du navigateur (F12)
- **Base de données** : Vérifiez les migrations

## 📈 **EXEMPLES PRATIQUES**

### **Exemple 1 : Simulation Rapide**
```
Méthode : Monte Carlo
Échantillons : 100
Niveau de confiance : 0.95
Temps estimé : 10-30 secondes
```

### **Exemple 2 : Simulation Précise**
```
Méthode : Bootstrap
Échantillons : 1000
Niveau de confiance : 0.99
Temps estimé : 2-5 minutes
```

### **Exemple 3 : Simulation Production**
```
Méthode : Monte Carlo
Échantillons : 10000
Niveau de confiance : 0.999
Temps estimé : 10-30 minutes
```

## 🎓 **CONCEPTS THÉORIQUES**

### **Calcul de Provision**
```
Pour chaque période :
1. Somme_lending = Σ(dénomination × quantité_lending)
2. Somme_recovery = Σ(dénomination × quantité_recovery)
3. Différence = Somme_lending - Somme_recovery
4. Solde_cumulatif += Différence
5. Provision = max(Solde_cumulatif)
```

### **Méthode Monte Carlo**
- Génère des échantillons aléatoires
- Basé sur la distribution de Poisson
- Simule des scénarios futurs

### **Méthode Bootstrap**
- Rééchantillonne vos données historiques
- Avec remise (répétition possible)
- Préserve la structure de vos données

## 🔒 **SÉCURITÉ ET DONNÉES**

### **Protection des Données**
- Authentification obligatoire
- Données isolées par utilisateur
- Tokens sécurisés

### **Sauvegarde**
- Base de données SQLite locale
- Fichiers uploadés conservés
- Résultats persistants

### **Limitations**
- Taille max fichier : 10MB
- Échantillons max : 15,000
- Utilisateurs simultanés : Illimité

## 📞 **SUPPORT ET AIDE**

### **En Cas de Problème**
1. Vérifiez ce guide
2. Consultez les logs d'erreur
3. Redémarrez l'application
4. Vérifiez les dépendances

### **Dépendances Requises**
- **Python** : 3.8+ (3.13 recommandé)
- **Node.js** : 16+ (18+ recommandé)
- **RAM** : 4GB minimum (8GB recommandé)
- **Espace disque** : 1GB minimum

### **Compatibilité**
- **OS** : Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Navigateurs** : Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

---

## 🎉 **FÉLICITATIONS !**

Vous maîtrisez maintenant l'application d'analyse de risque de crédit ! 

**Bonne analyse et bonnes simulations !** 🚀


