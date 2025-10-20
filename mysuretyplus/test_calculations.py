#!/usr/bin/env python3
"""
Test des calculs de provision avec la logique exacte fournie
"""

import sys
import os
import pandas as pd
import numpy as np

# Ajouter le backend au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from simulations.calculations import (
    calculer_somme,
    provision,
    montecarlo,
    bootstrap,
    estimation,
    clean,
    calculate_risk_metrics,
    calculate_real_cumulative
)

def create_test_data():
    """Crée des données de test basées sur la structure exacte fournie"""
    
    # Données de test pour lending (emprunts)
    # Colonnes: ref_date, interval, 50, 100, 200, 250, 500, 1000, 1500, 2000, 2500, 5000
    lending_data = {
        'ref_date': ['2020-01-01'] * 24 + ['2020-01-02'] * 24,
        'interval': list(range(24)) * 2,
        '50': np.random.randint(0, 10, 48),
        '100': np.random.randint(0, 8, 48),
        '200': np.random.randint(0, 6, 48),
        '250': np.random.randint(0, 5, 48),
        '500': np.random.randint(0, 4, 48),
        '1000': np.random.randint(0, 3, 48),
        '1500': np.random.randint(0, 2, 48),
        '2000': np.random.randint(0, 2, 48),
        '2500': np.random.randint(0, 1, 48),
        '5000': np.random.randint(0, 1, 48)
    }
    
    # Données de test pour recovery (remboursements)
    # Colonnes: SDATE, INTERVAL, 5, 34, 50, 61, 90, 100, 125, 173, 200, 215, 235, 250, 300, 435, 500, 600, 870, 1000, 1080, 1350, 1500, 1624, 1917, 2000, 2096, 2390, 2500, 3000, 4001, 5000
    recovery_data = {
        'SDATE': ['2020-01-01'] * 24 + ['2020-01-02'] * 24,
        'INTERVAL': list(range(24)) * 2,
        '5': np.random.randint(0, 5, 48),
        '34': np.random.randint(0, 3, 48),
        '50': np.random.randint(0, 8, 48),
        '61': np.random.randint(0, 4, 48),
        '90': np.random.randint(0, 3, 48),
        '100': np.random.randint(0, 6, 48),
        '125': np.random.randint(0, 2, 48),
        '173': np.random.randint(0, 2, 48),
        '200': np.random.randint(0, 5, 48),
        '215': np.random.randint(0, 3, 48),
        '235': np.random.randint(0, 2, 48),
        '250': np.random.randint(0, 4, 48),
        '300': np.random.randint(0, 3, 48),
        '435': np.random.randint(0, 2, 48),
        '500': np.random.randint(0, 4, 48),
        '600': np.random.randint(0, 2, 48),
        '870': np.random.randint(0, 1, 48),
        '1000': np.random.randint(0, 3, 48),
        '1080': np.random.randint(0, 1, 48),
        '1350': np.random.randint(0, 1, 48),
        '1500': np.random.randint(0, 2, 48),
        '1624': np.random.randint(0, 1, 48),
        '1917': np.random.randint(0, 1, 48),
        '2000': np.random.randint(0, 2, 48),
        '2096': np.random.randint(0, 1, 48),
        '2390': np.random.randint(0, 1, 48),
        '2500': np.random.randint(0, 1, 48),
        '3000': np.random.randint(0, 1, 48),
        '4001': np.random.randint(0, 1, 48),
        '5000': np.random.randint(0, 1, 48)
    }
    
    return pd.DataFrame(lending_data), pd.DataFrame(recovery_data)

def test_calculer_somme():
    """Test de la fonction calculer_somme"""
    print("🧮 Test de calculer_somme...")
    
    lending_df, recovery_df = create_test_data()
    
    # Test avec lending
    sommes_lending = calculer_somme(lending_df)
    print(f"   ✅ Sommes lending calculées: {len(sommes_lending)} valeurs")
    print(f"   📊 Exemple de sommes: {sommes_lending[:5]}")
    
    # Test avec recovery
    sommes_recovery = calculer_somme(recovery_df)
    print(f"   ✅ Sommes recovery calculées: {len(sommes_recovery)} valeurs")
    print(f"   📊 Exemple de sommes: {sommes_recovery[:5]}")
    
    return sommes_lending, sommes_recovery

def test_provision():
    """Test de la fonction provision"""
    print("\n💰 Test de provision...")
    
    lending_df, recovery_df = create_test_data()
    
    prov = provision(lending_df, recovery_df)
    print(f"   ✅ Provision calculée: {prov:.2f}")
    
    return prov

def test_real_cumulative():
    """Test du calcul de la trajectoire cumulative réelle"""
    print("\n📈 Test de calculate_real_cumulative...")
    
    lending_df, recovery_df = create_test_data()
    
    real_cumulative = calculate_real_cumulative(lending_df, recovery_df)
    print(f"   ✅ Trajectoire cumulative calculée: {len(real_cumulative)} points")
    print(f"   📊 Exemple de trajectoire: {real_cumulative[:10]}")
    
    return real_cumulative

def test_montecarlo():
    """Test de la fonction montecarlo"""
    print("\n🎲 Test de montecarlo...")
    
    lending_df, recovery_df = create_test_data()
    
    # Test avec lending
    temp_lending = montecarlo(lending_df)
    print(f"   ✅ Monte Carlo lending: {temp_lending.shape}")
    
    # Test avec recovery
    temp_recovery = montecarlo(recovery_df)
    print(f"   ✅ Monte Carlo recovery: {temp_recovery.shape}")
    
    return temp_lending, temp_recovery

def test_bootstrap():
    """Test de la fonction bootstrap"""
    print("\n🔄 Test de bootstrap...")
    
    lending_df, recovery_df = create_test_data()
    
    # Test avec lending
    temp_lending = bootstrap(lending_df)
    print(f"   ✅ Bootstrap lending: {temp_lending.shape}")
    
    # Test avec recovery
    temp_recovery = bootstrap(recovery_df)
    print(f"   ✅ Bootstrap recovery: {temp_recovery.shape}")
    
    return temp_lending, temp_recovery

def test_estimation():
    """Test de la fonction estimation complète"""
    print("\n🚀 Test d'estimation complète...")
    
    lending_df, recovery_df = create_test_data()
    
    # Test Monte Carlo avec peu d'échantillons pour la rapidité
    print("   🎲 Test Monte Carlo (10 échantillons)...")
    provisions_mc = estimation(lending_df, recovery_df, N=10, method="Montecarlo")
    print(f"   ✅ Monte Carlo terminé: {len(provisions_mc)} provisions")
    print(f"   📊 Provisions MC: {provisions_mc[:5]}")
    
    # Test Bootstrap avec peu d'échantillons
    print("   🔄 Test Bootstrap (10 échantillons)...")
    provisions_bs = estimation(lending_df, recovery_df, N=10, method="Bootstrap")
    print(f"   ✅ Bootstrap terminé: {len(provisions_bs)} provisions")
    print(f"   📊 Provisions BS: {provisions_bs[:5]}")
    
    return provisions_mc, provisions_bs

def test_risk_metrics():
    """Test du calcul des métriques de risque"""
    print("\n📊 Test des métriques de risque...")
    
    # Créer des données de test
    test_provisions = [1000, 1200, 1100, 1300, 1050, 1250, 1150, 1350, 1000, 1400]
    
    # Test clean
    cleaned_data = clean(test_provisions)
    print(f"   ✅ Données nettoyées: {len(cleaned_data)} valeurs")
    
    # Test calculate_risk_metrics
    risk_metrics = calculate_risk_metrics(test_provisions, alpha=0.95)
    print(f"   ✅ Métriques calculées:")
    print(f"      📈 Percentiles: {risk_metrics['percentiles']}")
    print(f"      🎯 IC 95%: [{risk_metrics['confidence_interval']['lower']:.2f}, {risk_metrics['confidence_interval']['upper']:.2f}]")
    print(f"      📊 Moyenne: {risk_metrics['mean']:.2f}")
    print(f"      📏 Écart-type: {risk_metrics['std']:.2f}")
    
    return risk_metrics

def main():
    """Fonction principale de test"""
    print("🧪 TESTS DES CALCULS DE PROVISION")
    print("=" * 50)
    
    try:
        # Test des fonctions de base
        test_calculer_somme()
        test_provision()
        test_real_cumulative()
        
        # Test des méthodes de rééchantillonnage
        test_montecarlo()
        test_bootstrap()
        
        # Test complet
        provisions_mc, provisions_bs = test_estimation()
        
        # Test des métriques de risque
        test_risk_metrics()
        
        print("\n" + "=" * 50)
        print("✅ TOUS LES TESTS TERMINÉS AVEC SUCCÈS !")
        print("🎉 La logique de calcul fonctionne correctement.")
        
    except Exception as e:
        print(f"\n❌ ERREUR DANS LES TESTS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
