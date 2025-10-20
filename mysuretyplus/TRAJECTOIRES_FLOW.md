# 🔄 Flux de Données - Tracé des Trajectoires

## 📊 Diagramme de Flux

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Fichiers CSV  │    │   Prétraitement  │    │  Calcul Flux    │
│                 │    │                  │    │                 │
│ lending.csv     │───▶│ load_and_        │───▶│ calculate_      │
│ recovery.csv    │    │ preprocess_data  │    │ cash_flow       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Simulations   │    │  Génération      │    │  Trajectoires   │
│                 │    │  Avancées        │    │  Simulées       │
│ Monte Carlo     │◀───│ generate_        │◀───│ calculate_      │
│ Bootstrap       │    │ simulations_     │    │ cash_flow       │
└─────────────────┘    │ avance           │    └─────────────────┘
                       └──────────────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │  Génération      │
                       │  Graphique       │
                       │                  │
                       │ generate_        │
                       │ trajectory_plot  │
                       └──────────────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │  Image Base64    │
                       │                  │
                       │ matplotlib       │
                       │ → base64         │
                       └──────────────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │  Frontend        │
                       │                  │
                       │ Affichage        │
                       │ + Statistiques   │
                       └──────────────────┘
```

## 🔧 Fonctions Principales

### 1. **Prétraitement des Données**
```python
load_and_preprocess_data(lending_df, recovery_df)
├── Nettoyage des noms de colonnes
├── Conversion des colonnes numériques
└── Retour des DataFrames prétraités
```

### 2. **Calcul du Flux de Trésorerie**
```python
calculate_cash_flow(lending_df, recovery_df)
├── Calcul des montants totaux (calculer_somme)
├── Création des identifiants datetime
├── Fusion des données lending/recovery
├── Calcul du flux net (emprunts - remboursements)
└── Calcul de la trajectoire cumulative
```

### 3. **Génération des Simulations**
```python
generate_simulations_avance(original_lending, original_recovery, n_simulations, method)
├── Pour chaque simulation:
│   ├── Monte Carlo: montecarlo_ameliore()
│   └── Bootstrap: bootstrap_ameliore()
└── Retour des listes de DataFrames simulés
```

### 4. **Génération du Graphique**
```python
generate_trajectory_plot(lending_df, recovery_df, method, num_trajectories)
├── Prétraitement des données
├── Génération des simulations
├── Calcul des trajectoires (originale + simulées)
├── Création du graphique matplotlib
├── Conversion en base64
└── Calcul des statistiques
```

## 📈 Données de Sortie

### **Trajectoire Originale**
- **Index** : Position temporelle des transactions
- **Cumulative Flow** : Montant cumulé au fil du temps
- **Couleur** : Bleu foncé (ligne épaisse)

### **Trajectoires Simulées**
- **Index** : Même structure temporelle que l'originale
- **Cumulative Flow** : Montants cumulés simulés
- **Couleur** : Bleu clair (lignes fines, transparence)

### **Statistiques**
- **Valeur Finale Originale** : Montant cumulé final des données réelles
- **Moyenne Simulée** : Moyenne des valeurs finales des simulations
- **Écart-Type** : Variabilité des simulations
- **IC 95%** : Intervalle de confiance à 95%

## 🎯 Points d'Intégration

### **Backend (Django)**
1. **calculations.py** : Nouvelles fonctions de calcul
2. **views.py** : Génération dans SimulationResultsView
3. **API Response** : Ajout des données trajectory_plot

### **Frontend (React)**
1. **SimulationResults.js** : Affichage du graphique
2. **Interface** : Statistiques et indicateurs
3. **Gestion d'erreurs** : Fallback en cas d'échec

## ⚡ Optimisations

### **Performance**
- **Génération côté backend** : Évite la surcharge du frontend
- **Cache des images** : Réutilisation des graphiques générés
- **Limitation du nombre de trajectoires** : 20 max pour l'affichage

### **Mémoire**
- **Fermeture des figures** : plt.close() après génération
- **Buffer mémoire** : io.BytesIO() pour la conversion
- **Nettoyage automatique** : Gestion des ressources

## 🔍 Points de Contrôle

### **Validation des Données**
- Vérification de la structure des DataFrames
- Validation des colonnes numériques
- Gestion des valeurs manquantes

### **Gestion d'Erreurs**
- Try-catch dans toutes les fonctions
- Messages d'erreur descriptifs
- Fallback gracieux en cas d'échec

### **Tests**
- Tests unitaires pour chaque fonction
- Tests d'intégration end-to-end
- Validation des données de sortie
