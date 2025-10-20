#!/usr/bin/env python3
"""
Script de test pour vérifier le fonctionnement de la simulation
"""

import sys
import os
import pandas as pd
import numpy as np

# Ajouter le chemin du backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from simulations.calculations import (
    calculer_somme, 
    provision, 
    montecarlo, 
    bootstrap, 
    estimation,
    calculate_risk_metrics,
    get_provision_for_risk_level,
    get_risk_level_for_provision
)

def create_test_data():
    """Créer des données de test"""
    print("🔧 Création des données de test...")
    
    # Données de test pour lending (emprunts)
    lending_data = {
        'ref_date': ['2020-01-01'] * 24 + ['2020-01-02'] * 24,
        'interval': list(range(24)) * 2,
        '50': np.random.randint(0, 10, 48),
        '100': np.random.randint(0, 15, 48),
        '200': np.random.randint(0, 20, 48),
        '250': np.random.randint(0, 25, 48),
        '500': np.random.randint(0, 30, 48),
        '1000': np.random.randint(0, 35, 48),
        '1500': np.random.randint(0, 40, 48),
        '2000': np.random.randint(0, 45, 48),
        '2500': np.random.randint(0, 50, 48),
        '5000': np.random.randint(0, 55, 48)
    }
    
    # Données de test pour recovery (remboursements)
    recovery_data = {
        'SDATE': ['2020-01-01'] * 24 + ['2020-01-02'] * 24,
        'INTERVAL': list(range(24)) * 2,
        '5': np.random.randint(0, 5, 48),
        '34': np.random.randint(0, 8, 48),
        '50': np.random.randint(0, 10, 48),
        '61': np.random.randint(0, 12, 48),
        '90': np.random.randint(0, 15, 48),
        '100': np.random.randint(0, 18, 48),
        '125': np.random.randint(0, 20, 48),
        '173': np.random.randint(0, 25, 48),
        '200': np.random.randint(0, 30, 48),
        '215': np.random.randint(0, 35, 48),
        '235': np.random.randint(0, 40, 48),
        '250': np.random.randint(0, 45, 48),
        '300': np.random.randint(0, 50, 48),
        '435': np.random.randint(0, 55, 48),
        '500': np.random.randint(0, 60, 48),
        '600': np.random.randint(0, 65, 48),
        '870': np.random.randint(0, 70, 48),
        '1000': np.random.randint(0, 75, 48),
        '1080': np.random.randint(0, 80, 48),
        '1350': np.random.randint(0, 85, 48),
        '1500': np.random.randint(0, 90, 48),
        '1624': np.random.randint(0, 95, 48),
        '1917': np.random.randint(0, 100, 48),
        '2000': np.random.randint(0, 105, 48),
        '2096': np.random.randint(0, 110, 48),
        '2390': np.random.randint(0, 115, 48),
        '2500': np.random.randint(0, 120, 48),
        '3000': np.random.randint(0, 125, 48),
        '4001': np.random.randint(0, 130, 48),
        '5000': np.random.randint(0, 135, 48)
    }
    
    lending_df = pd.DataFrame(lending_data)
    recovery_df = pd.DataFrame(recovery_data)
    
    print(f"✅ Données créées - Lending: {lending_df.shape}, Recovery: {recovery_df.shape}")
    return lending_df, recovery_df

def test_calculations():
    """Tester toutes les fonctions de calcul"""
    print("\n🧪 Test des fonctions de calcul...")
    
    # Créer les données de test
    lending_df, recovery_df = create_test_data()
    
    # Test 1: calculer_somme
    print("\n1️⃣ Test de calculer_somme...")
    try:
        sommes_lending = calculer_somme(lending_df)
        sommes_recovery = calculer_somme(recovery_df)
        print(f"✅ Sommes calculées - Lending: {len(sommes_lending)}, Recovery: {len(sommes_recovery)}")
        print(f"   Exemple lending: {sommes_lending[:3]}")
        print(f"   Exemple recovery: {sommes_recovery[:3]}")
    except Exception as e:
        print(f"❌ Erreur dans calculer_somme: {e}")
        return False
    
    # Test 2: provision
    print("\n2️⃣ Test de provision...")
    try:
        real_provision = provision(lending_df, recovery_df)
        print(f"✅ Provision réelle calculée: {real_provision}")
    except Exception as e:
        print(f"❌ Erreur dans provision: {e}")
        return False
    
    # Test 3: montecarlo
    print("\n3️⃣ Test de montecarlo...")
    try:
        monte_carlo_lending = montecarlo(lending_df)
        monte_carlo_recovery = montecarlo(recovery_df)
        print(f"✅ Monte Carlo - Lending: {monte_carlo_lending.shape}, Recovery: {monte_carlo_recovery.shape}")
    except Exception as e:
        print(f"❌ Erreur dans montecarlo: {e}")
        return False
    
    # Test 4: bootstrap
    print("\n4️⃣ Test de bootstrap...")
    try:
        bootstrap_lending = bootstrap(lending_df)
        bootstrap_recovery = bootstrap(recovery_df)
        print(f"✅ Bootstrap - Lending: {bootstrap_lending.shape}, Recovery: {bootstrap_recovery.shape}")
    except Exception as e:
        print(f"❌ Erreur dans bootstrap: {e}")
        return False
    
    # Test 5: estimation Monte Carlo
    print("\n5️⃣ Test d'estimation Monte Carlo...")
    try:
        provisions_mc = estimation(lending_df, recovery_df, N=100, method="Montecarlo")
        print(f"✅ Monte Carlo - {len(provisions_mc)} provisions calculées")
        print(f"   Provision réelle: {provisions_mc[0]}")
        print(f"   Provisions simulées: {provisions_mc[1:5]}...")
        
        # Test des métriques de risque
        risk_metrics = calculate_risk_metrics(provisions_mc[1:], 0.95)
        print(f"✅ Métriques de risque calculées:")
        print(f"   Percentiles: {risk_metrics['percentiles']}")
        print(f"   Intervalle de confiance: {risk_metrics['confidence_interval']}")
        
    except Exception as e:
        print(f"❌ Erreur dans estimation Monte Carlo: {e}")
        return False
    
    # Test 6: estimation Bootstrap
    print("\n6️⃣ Test d'estimation Bootstrap...")
    try:
        provisions_bs = estimation(lending_df, recovery_df, N=100, method="Bootstrap")
        print(f"✅ Bootstrap - {len(provisions_bs)} provisions calculées")
        print(f"   Provision réelle: {provisions_bs[0]}")
        print(f"   Provisions simulées: {provisions_bs[1:5]}...")
        
    except Exception as e:
        print(f"❌ Erreur dans estimation Bootstrap: {e}")
        return False
    
    # Test 7: Calculs de risque
    print("\n7️⃣ Test des calculs de risque...")
    try:
        simulated_provisions = provisions_mc[1:]  # Exclure la provision réelle
        
        # Test provision pour risque
        risk_level = 5.0
        provision_value = get_provision_for_risk_level(simulated_provisions, risk_level)
        print(f"✅ Pour un risque de {risk_level}%, provision nécessaire: {provision_value}")
        
        # Test risque pour provision
        target_provision = provision_value
        calculated_risk = get_risk_level_for_provision(simulated_provisions, target_provision)
        print(f"✅ Pour une provision de {target_provision}, risque calculé: {calculated_risk}%")
        
    except Exception as e:
        print(f"❌ Erreur dans les calculs de risque: {e}")
        return False
    
    print("\n🎉 Tous les tests sont passés avec succès!")
    return True

if __name__ == "__main__":
    print("🚀 Démarrage des tests de simulation...")
    success = test_calculations()
    
    if success:
        print("\n✅ Tous les tests sont réussis! L'application devrait fonctionner correctement.")
    else:
        print("\n❌ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    # Vérifier si les fichiers CSV ont été créés
    print("\n📁 Vérification des fichiers générés...")
    if os.path.exists('provisions_montecarlo.csv'):
        print("✅ provisions_montecarlo.csv créé")
    else:
        print("❌ provisions_montecarlo.csv non trouvé")
    
    if os.path.exists('provisions_bootstrap.csv'):
        print("✅ provisions_bootstrap.csv créé")
    else:
        print("❌ provisions_bootstrap.csv non trouvé")

