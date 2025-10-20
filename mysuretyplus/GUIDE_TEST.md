# 🧪 GUIDE DE TEST - APPLICATION NANA

## 🎯 **STATUT ACTUEL : PROBLÈME RÉSOLU !**

### ✅ **Problèmes Corrigés :**
1. **ID de simulation undefined** → ✅ Corrigé
2. **Provisions simulées = 0** → ✅ Corrigé  
3. **Densité vide** → ✅ Corrigé
4. **Calculs de risque** → ✅ Corrigé

### 🔧 **Corrections Apportées :**
- ✅ Fonction `estimation` corrigée pour reconnaître les méthodes en minuscules
- ✅ Logs de debug ajoutés dans le frontend et backend
- ✅ Vérification de l'ID avant monitoring
- ✅ Simulation ID 22 recalculée avec succès (10 provisions simulées)

---

## 🚀 **TEST DE L'APPLICATION**

### **1. Lancement de l'Application**
```bash
# Option 1: Script automatique
start_fixed.bat

# Option 2: Manuel
# Terminal 1 (Backend)
cd backend
python manage.py runserver

# Terminal 2 (Frontend)  
cd frontend
npm start
```

### **2. Test d'Authentification**
1. Allez sur http://localhost:3000
2. Créez un compte ou connectez-vous
3. ✅ Vérifiez que vous accédez au dashboard

### **3. Test d'Upload de Fichiers**
1. Cliquez sur "Télécharger des fichiers"
2. Uploadez vos fichiers CSV :
   - **Lending** : `TABLE_LENDING_012020_032020.csv`
   - **Recovery** : `recovery_summary_012020_032020.csv`
3. ✅ Vérifiez que les fichiers sont validés

### **4. Test de Simulation**
1. Cliquez sur "Lancer une simulation"
2. Configurez :
   - **Méthode** : Monte Carlo
   - **Échantillons** : 10 (pour test rapide)
   - **Alpha** : 0.95
3. Cliquez sur "Lancer la simulation"
4. ✅ Vérifiez que l'ID de simulation est affiché dans la console

### **5. Vérification des Résultats**
1. Attendez que la simulation se termine
2. Vérifiez dans la console du navigateur :
   ```
   🔍 SimulationForm - ID de simulation: [NUMBER]
   🔍 SimulationResults - Provisions simulées: [NUMBER > 0]
   ```

### **6. Test des Graphiques**
1. **Graphique de trajectoire** :
   - ✅ Ligne réelle (couleur distincte)
   - ✅ Lignes simulées (faisceau de couleurs différentes)

2. **Graphique de densité** :
   - ✅ Courbe de densité visible
   - ✅ Zones de risque colorées (5%, 2.5%, 1%)

### **7. Test du Calculateur de Risque**
1. Allez dans "Calculer le risque"
2. **Test 1** : Entrez un niveau de risque (ex: 5%)
   - ✅ Doit afficher la provision correspondante
3. **Test 2** : Entrez une provision
   - ✅ Doit afficher le niveau de risque correspondant

---

## 🔍 **DEBUG ET VÉRIFICATION**

### **Logs Frontend (Console Navigateur)**
```javascript
// Logs attendus :
🔍 SimulationForm - Réponse du backend: {id: 23, method: "montecarlo", ...}
🔍 SimulationForm - ID de simulation: 23
🔍 Dashboard - Simulation reçue: {id: 23, ...}
🔍 SimulationResults - Provisions simulées: 10
🔍 SimulationResults - Trajectoires simulées: 10
```

### **Logs Backend (Terminal)**
```python
# Logs attendus :
🔍 SimulationListCreateView - Création d'une nouvelle simulation
✅ Simulation créée avec ID: 23
🚀 Lancement de 10 simulations Monte Carlo...
✅ 11 provisions Monte Carlo calculées
🎉 Estimation terminée - 11 provisions au total
```

### **Vérification Base de Données**
```bash
python check_simulation.py
# Doit afficher :
# Provisions simulées: 10 valeurs
# Percentiles: 9 clés
# Intervalle de confiance: 3 clés
```

---

## 🎯 **RÉSULTATS ATTENDUS**

### **✅ Succès :**
- Simulation créée avec ID valide
- 10+ provisions simulées générées
- Graphiques avec données réelles ET simulées
- Calculateur de risque fonctionnel
- Densité de provision visible

### **❌ Échec :**
- ID undefined dans les logs
- Provisions simulées = 0
- Graphiques vides
- Erreurs 404 répétées

---

## 🆘 **EN CAS DE PROBLÈME**

### **1. Si ID undefined :**
```bash
# Vérifier la base de données
python check_simulation.py
```

### **2. Si provisions = 0 :**
```bash
# Forcer le recalcul
python force_simulation.py
```

### **3. Si erreurs 404 :**
- Vérifier que le backend tourne sur http://localhost:8000
- Vérifier l'authentification (token valide)

### **4. Si graphiques vides :**
- Vérifier les logs frontend pour les données reçues
- Vérifier que `simulated_provisions.length > 0`

---

## 📊 **DONNÉES DE TEST**

### **Simulation ID 22 (Corrigée) :**
- ✅ Provision réelle : 257,733,403
- ✅ 10 provisions simulées : [259,620,022, 256,876,566, ...]
- ✅ 9 percentiles calculés
- ✅ 3 intervalles de confiance
- ✅ 2184 points de trajectoire

### **Nouvelles Simulations :**
- Devraient générer des résultats similaires
- Temps de calcul : ~1-2 secondes pour 10 échantillons
- Temps de calcul : ~30-60 secondes pour 1000 échantillons

---

## 🎉 **CONCLUSION**

L'application devrait maintenant fonctionner correctement avec :
- ✅ Simulations qui génèrent des données
- ✅ Graphiques avec trajectoires réelles et simulées  
- ✅ Courbe de densité avec zones de risque
- ✅ Calculateur de risque bidirectionnel
- ✅ Interface utilisateur réactive

**Testez maintenant et confirmez que tout fonctionne !** 🚀
