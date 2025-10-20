#!/usr/bin/env python3
"""
Script de test pour l'intégration du tracé des trajectoires des montants cumulés
"""

import sys
import os
import pandas as pd
import numpy as np

# Ajouter le chemin du backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Importer les fonctions de calcul
from simulations.calculations import (
    load_and_preprocess_data,
    calculate_cash_flow,
    generate_simulations_avance,
    generate_trajectory_plot
)

def create_test_data():
    """Crée des données de test pour les simulations"""
    print("🔧 Création des données de test...")
    
    # Données de test pour lending
    lending_data = {
        'ref_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
        'INTERVAL': [1, 1, 1, 1, 1],
        '50': [10, 5, 8, 12, 6],
        '100': [5, 3, 4, 7, 2],
        '200': [2, 1, 1, 3, 1],
        '500': [1, 0, 1, 2, 0]
    }
    
    # Données de test pour recovery
    recovery_data = {
        'SDATE': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
        'INTERVAL': [1, 1, 1, 1, 1],
        '50': [8, 4, 6, 10, 5],
        '100': [3, 2, 3, 5, 1],
        '200': [1, 1, 0, 2, 1],
        '500': [0, 0, 1, 1, 0]
    }
    
    lending_df = pd.DataFrame(lending_data)
    recovery_df = pd.DataFrame(recovery_data)
    
    print(f"✅ Données de test créées:")
    print(f"   Lending: {lending_df.shape}")
    print(f"   Recovery: {recovery_df.shape}")
    
    return lending_df, recovery_df

def test_cash_flow_calculation():
    """Teste le calcul du flux de trésorerie"""
    print("\n🧮 Test du calcul du flux de trésorerie...")
    
    lending_df, recovery_df = create_test_data()
    
    # Prétraiter les données
    lending_processed, recovery_processed = load_and_preprocess_data(lending_df, recovery_df)
    
    # Calculer le flux de trésorerie
    cash_flow = calculate_cash_flow(lending_processed, recovery_processed)
    
    print(f"✅ Flux de trésorerie calculé:")
    print(f"   Nombre de transactions: {len(cash_flow)}")
    print(f"   Flux net total: {cash_flow['net_flow'].sum():,.2f}")
    print(f"   Valeur cumulative finale: {cash_flow['cumulative_flow'].iloc[-1]:,.2f}")
    
    return cash_flow

def test_simulations_generation():
    """Teste la génération des simulations"""
    print("\n🎲 Test de la génération des simulations...")
    
    lending_df, recovery_df = create_test_data()
    lending_processed, recovery_processed = load_and_preprocess_data(lending_df, recovery_df)
    
    # Générer des simulations
    n_simulations = 5
    simulated_lending_list, simulated_recovery_list = generate_simulations_avance(
        lending_processed, recovery_processed, n_simulations, 'montecarlo'
    )
    
    print(f"✅ Simulations générées:")
    print(f"   Nombre de simulations: {len(simulated_lending_list)}")
    print(f"   Structure lending: {simulated_lending_list[0].shape}")
    print(f"   Structure recovery: {simulated_recovery_list[0].shape}")
    
    return simulated_lending_list, simulated_recovery_list

def test_trajectory_plot_generation():
    """Teste la génération du graphique des trajectoires"""
    print("\n📊 Test de la génération du graphique des trajectoires...")
    
    lending_df, recovery_df = create_test_data()
    
    # Générer le graphique
    result = generate_trajectory_plot(
        lending_df=lending_df,
        recovery_df=recovery_df,
        method='montecarlo',
        num_trajectories=10
    )
    
    print(f"✅ Résultat de la génération:")
    print(f"   Succès: {result['success']}")
    print(f"   Message: {result['message']}")
    print(f"   Image générée: {'Oui' if result['image_base64'] else 'Non'}")
    print(f"   Taille image: {len(result['image_base64'])} caractères")
    
    if result['stats']:
        print(f"   Statistiques:")
        print(f"     Valeur finale originale: {result['stats'].get('original_final_value', 0):,.2f}")
        print(f"     Moyenne simulée: {result['stats'].get('simulated_mean', 0):,.2f}")
        print(f"     Écart-type: {result['stats'].get('simulated_std', 0):,.2f}")
        print(f"     IC 95%: {result['stats'].get('simulated_ci_95', [0, 0])}")
    
    return result

def main():
    """Fonction principale de test"""
    print("🚀 Test d'intégration du tracé des trajectoires des montants cumulés")
    print("=" * 70)
    
    try:
        # Test 1: Calcul du flux de trésorerie
        cash_flow = test_cash_flow_calculation()
        
        # Test 2: Génération des simulations
        simulated_lending, simulated_recovery = test_simulations_generation()
        
        # Test 3: Génération du graphique des trajectoires
        trajectory_result = test_trajectory_plot_generation()
        
        print("\n🎉 Tous les tests sont passés avec succès!")
        print("✅ L'intégration du tracé des trajectoires est fonctionnelle")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
