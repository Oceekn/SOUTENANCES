#!/usr/bin/env python3
"""
Script de debug pour identifier les problèmes de simulation
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
    calculate_risk_metrics
)

def debug_simulation():
    """Debug de la simulation"""
    print("🔍 DEBUG DE LA SIMULATION")
    print("=" * 50)
    
    # Créer des données de test simples
    print("\n1️⃣ Création des données de test...")
    
    # Données de test minimales
    lending_data = {
        'ref_date': ['2020-01-01'] * 24,
        'interval': list(range(24)),
        '50': [1] * 24,
        '100': [2] * 24,
        '200': [3] * 24,
        '250': [4] * 24,
        '500': [5] * 24,
        '1000': [6] * 24,
        '1500': [7] * 24,
        '2000': [8] * 24,
        '2500': [9] * 24,
        '5000': [10] * 24
    }
    
    recovery_data = {
        'SDATE': ['2020-01-01'] * 24,
        'INTERVAL': list(range(24)),
        '5': [0] * 24,
        '34': [1] * 24,
        '50': [2] * 24,
        '61': [3] * 24,
        '90': [4] * 24,
        '100': [5] * 24,
        '125': [6] * 24,
        '173': [7] * 24,
        '200': [8] * 24,
        '215': [9] * 24,
        '235': [10] * 24,
        '250': [11] * 24,
        '300': [12] * 24,
        '435': [13] * 24,
        '500': [14] * 24,
        '600': [15] * 24,
        '870': [16] * 24,
        '1000': [17] * 24,
        '1080': [18] * 24,
        '1350': [19] * 24,
        '1500': [20] * 24,
        '1624': [21] * 24,
        '1917': [22] * 24,
        '2000': [23] * 24,
        '2096': [24] * 24,
        '2390': [25] * 24,
        '2500': [26] * 24,
        '3000': [27] * 24,
        '4001': [28] * 24,
        '5000': [29] * 24
    }
    
    lending_df = pd.DataFrame(lending_data)
    recovery_df = pd.DataFrame(recovery_data)
    
    print(f"✅ Données créées - Lending: {lending_df.shape}, Recovery: {recovery_df.shape}")
    print(f"   Colonnes lending: {list(lending_df.columns)}")
    print(f"   Colonnes recovery: {list(recovery_df.columns)}")
    
    # Test 2: calculer_somme
    print("\n2️⃣ Test de calculer_somme...")
    try:
        sommes_lending = calculer_somme(lending_df)
        sommes_recovery = calculer_somme(recovery_df)
        print(f"✅ Sommes calculées - Lending: {len(sommes_lending)}, Recovery: {len(sommes_recovery)}")
        print(f"   Exemple lending: {sommes_lending[:3]}")
        print(f"   Exemple recovery: {sommes_recovery[:3]}")
    except Exception as e:
        print(f"❌ Erreur dans calculer_somme: {e}")
        return False
    
    # Test 3: provision
    print("\n3️⃣ Test de provision...")
    try:
        real_provision = provision(lending_df, recovery_df)
        print(f"✅ Provision réelle calculée: {real_provision}")
    except Exception as e:
        print(f"❌ Erreur dans provision: {e}")
        return False
    
    # Test 4: estimation Monte Carlo avec peu d'échantillons
    print("\n4️⃣ Test d'estimation Monte Carlo (10 échantillons)...")
    try:
        provisions_mc = estimation(lending_df, recovery_df, N=10, method="Montecarlo")
        print(f"✅ Monte Carlo - {len(provisions_mc)} provisions calculées")
        print(f"   Provision réelle: {provisions_mc[0]}")
        print(f"   Provisions simulées: {provisions_mc[1:]}")
        
        if len(provisions_mc) > 1:
            # Test des métriques de risque
            risk_metrics = calculate_risk_metrics(provisions_mc[1:], 0.95)
            print(f"✅ Métriques de risque calculées:")
            print(f"   Percentiles: {risk_metrics['percentiles']}")
            print(f"   Intervalle de confiance: {risk_metrics['confidence_interval']}")
        else:
            print("❌ Aucune provision simulée générée!")
            
    except Exception as e:
        print(f"❌ Erreur dans estimation Monte Carlo: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: estimation Bootstrap avec peu d'échantillons
    print("\n5️⃣ Test d'estimation Bootstrap (10 échantillons)...")
    try:
        provisions_bs = estimation(lending_df, recovery_df, N=10, method="Bootstrap")
        print(f"✅ Bootstrap - {len(provisions_bs)} provisions calculées")
        print(f"   Provision réelle: {provisions_bs[0]}")
        print(f"   Provisions simulées: {provisions_bs[1:]}")
        
        if len(provisions_bs) <= 1:
            print("❌ Aucune provision simulée générée!")
            
    except Exception as e:
        print(f"❌ Erreur dans estimation Bootstrap: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 Debug terminé!")
    return True

if __name__ == "__main__":
    print("🚀 Démarrage du debug de simulation...")
    success = debug_simulation()
    
    if success:
        print("\n✅ Le debug est réussi! Le problème n'est pas dans les calculs.")
    else:
        print("\n❌ Le debug a révélé des problèmes dans les calculs.")
    
    # Vérifier si les fichiers CSV ont été créés
    print("\n📁 Vérification des fichiers générés...")
    if os.path.exists('provisions_montecarlo.csv'):
        print("✅ provisions_montecarlo.csv créé")
        # Lire le contenu
        df = pd.read_csv('provisions_montecarlo.csv', sep=';')
        print(f"   Contenu: {len(df)} lignes")
        print(f"   Colonnes: {list(df.columns)}")
    else:
        print("❌ provisions_montecarlo.csv non trouvé")
    
    if os.path.exists('provisions_bootstrap.csv'):
        print("✅ provisions_bootstrap.csv créé")
        # Lire le contenu
        df = pd.read_csv('provisions_bootstrap.csv', sep=';')
        print(f"   Contenu: {len(df)} lignes")
        print(f"   Colonnes: {list(df.columns)}")
    else:
        print("❌ provisions_bootstrap.csv non trouvé")

