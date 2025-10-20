#!/usr/bin/env python3
"""
Script de démonstration du tracé des trajectoires des montants cumulés
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Ajouter le chemin du backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Importer les fonctions de calcul
from simulations.calculations import (
    load_and_preprocess_data,
    calculate_cash_flow,
    generate_simulations_avance,
    generate_trajectory_plot,
    plot_transaction_trajectories
)

def create_realistic_data():
    """Crée des données réalistes pour la démonstration"""
    print("🔧 Création de données réalistes...")
    
    # Générer des dates sur 3 mois
    dates = pd.date_range('2023-01-01', '2023-03-31', freq='D')
    
    # Données de lending (emprunts)
    lending_data = {
        'ref_date': dates.strftime('%Y-%m-%d').tolist(),
        'INTERVAL': [1] * len(dates),
        '50': np.random.poisson(5, len(dates)),
        '100': np.random.poisson(3, len(dates)),
        '200': np.random.poisson(2, len(dates)),
        '500': np.random.poisson(1, len(dates)),
        '1000': np.random.poisson(0.5, len(dates))
    }
    
    # Données de recovery (remboursements) - généralement plus faibles
    recovery_data = {
        'SDATE': dates.strftime('%Y-%m-%d').tolist(),
        'INTERVAL': [1] * len(dates),
        '50': np.random.poisson(4, len(dates)),
        '100': np.random.poisson(2, len(dates)),
        '200': np.random.poisson(1, len(dates)),
        '500': np.random.poisson(0.5, len(dates)),
        '1000': np.random.poisson(0.2, len(dates))
    }
    
    lending_df = pd.DataFrame(lending_data)
    recovery_df = pd.DataFrame(recovery_data)
    
    print(f"✅ Données réalistes créées:")
    print(f"   Période: {dates[0].strftime('%Y-%m-%d')} à {dates[-1].strftime('%Y-%m-%d')}")
    print(f"   Lending: {lending_df.shape}")
    print(f"   Recovery: {recovery_df.shape}")
    
    return lending_df, recovery_df

def demonstrate_cash_flow():
    """Démontre le calcul du flux de trésorerie"""
    print("\n💰 Démonstration du calcul du flux de trésorerie...")
    
    lending_df, recovery_df = create_realistic_data()
    
    # Prétraiter les données
    lending_processed, recovery_processed = load_and_preprocess_data(lending_df, recovery_df)
    
    # Calculer le flux de trésorerie
    cash_flow = calculate_cash_flow(lending_processed, recovery_processed)
    
    print(f"✅ Flux de trésorerie calculé:")
    print(f"   Nombre de transactions: {len(cash_flow)}")
    print(f"   Emprunts totaux: {cash_flow['total_lending'].sum():,.2f} XAF")
    print(f"   Remboursements totaux: {cash_flow['total_recovery'].sum():,.2f} XAF")
    print(f"   Flux net total: {cash_flow['net_flow'].sum():,.2f} XAF")
    print(f"   Valeur cumulative finale: {cash_flow['cumulative_flow'].iloc[-1]:,.2f} XAF")
    
    # Afficher les premières lignes
    print(f"\n📊 Premières lignes du flux de trésorerie:")
    print(cash_flow.head())
    
    return cash_flow

def demonstrate_simulations():
    """Démontre la génération des simulations"""
    print("\n🎲 Démonstration de la génération des simulations...")
    
    lending_df, recovery_df = create_realistic_data()
    lending_processed, recovery_processed = load_and_preprocess_data(lending_df, recovery_df)
    
    # Générer des simulations
    n_simulations = 10
    print(f"   Génération de {n_simulations} simulations Monte Carlo...")
    
    simulated_lending_list, simulated_recovery_list = generate_simulations_avance(
        lending_processed, recovery_processed, n_simulations, 'montecarlo'
    )
    
    print(f"✅ Simulations générées:")
    print(f"   Nombre de simulations: {len(simulated_lending_list)}")
    print(f"   Structure lending: {simulated_lending_list[0].shape}")
    print(f"   Structure recovery: {simulated_recovery_list[0].shape}")
    
    # Calculer les trajectoires simulées
    simulated_flows = []
    for i in range(len(simulated_lending_list)):
        sim_flow = calculate_cash_flow(simulated_lending_list[i], simulated_recovery_list[i])
        simulated_flows.append(sim_flow)
    
    # Statistiques des simulations
    final_values = [flow['cumulative_flow'].iloc[-1] for flow in simulated_flows]
    print(f"\n📈 Statistiques des simulations:")
    print(f"   Valeur finale moyenne: {np.mean(final_values):,.2f} XAF")
    print(f"   Écart-type: {np.std(final_values):,.2f} XAF")
    print(f"   Min: {np.min(final_values):,.2f} XAF")
    print(f"   Max: {np.max(final_values):,.2f} XAF")
    
    return simulated_lending_list, simulated_recovery_list

def demonstrate_plotting():
    """Démontre la génération des graphiques"""
    print("\n📊 Démonstration de la génération des graphiques...")
    
    lending_df, recovery_df = create_realistic_data()
    
    # Générer le graphique des trajectoires
    print("   Génération du graphique des trajectoires...")
    result = generate_trajectory_plot(
        lending_df=lending_df,
        recovery_df=recovery_df,
        method='montecarlo',
        num_trajectories=15
    )
    
    print(f"✅ Graphique généré:")
    print(f"   Succès: {result['success']}")
    print(f"   Taille image: {len(result['image_base64'])} caractères")
    
    if result['stats']:
        print(f"\n📈 Statistiques du graphique:")
        print(f"   Valeur finale originale: {result['stats']['original_final_value']:,.2f} XAF")
        print(f"   Moyenne simulée: {result['stats']['simulated_mean']:,.2f} XAF")
        print(f"   Écart-type: {result['stats']['simulated_std']:,.2f} XAF")
        print(f"   IC 95%: [{result['stats']['simulated_ci_95'][0]:,.2f}, {result['stats']['simulated_ci_95'][1]:,.2f}] XAF")
        print(f"   Nombre de transactions: {result['stats']['num_transactions']}")
        print(f"   Nombre de simulations: {result['stats']['num_simulations']}")
    
    return result

def demonstrate_comparison():
    """Démontre la comparaison entre Monte Carlo et Bootstrap"""
    print("\n🔄 Démonstration de la comparaison Monte Carlo vs Bootstrap...")
    
    lending_df, recovery_df = create_realistic_data()
    
    # Monte Carlo
    print("   Génération Monte Carlo...")
    mc_result = generate_trajectory_plot(
        lending_df=lending_df,
        recovery_df=recovery_df,
        method='montecarlo',
        num_trajectories=10
    )
    
    # Bootstrap
    print("   Génération Bootstrap...")
    bs_result = generate_trajectory_plot(
        lending_df=lending_df,
        recovery_df=recovery_df,
        method='bootstrap',
        num_trajectories=10
    )
    
    print(f"\n📊 Comparaison des méthodes:")
    print(f"   Monte Carlo:")
    print(f"     Succès: {mc_result['success']}")
    print(f"     Moyenne: {mc_result['stats']['simulated_mean']:,.2f} XAF")
    print(f"     Écart-type: {mc_result['stats']['simulated_std']:,.2f} XAF")
    
    print(f"   Bootstrap:")
    print(f"     Succès: {bs_result['success']}")
    print(f"     Moyenne: {bs_result['stats']['simulated_mean']:,.2f} XAF")
    print(f"     Écart-type: {bs_result['stats']['simulated_std']:,.2f} XAF")
    
    return mc_result, bs_result

def main():
    """Fonction principale de démonstration"""
    print("🚀 Démonstration du Tracé des Trajectoires des Montants Cumulés")
    print("=" * 70)
    
    try:
        # Démonstration 1: Calcul du flux de trésorerie
        cash_flow = demonstrate_cash_flow()
        
        # Démonstration 2: Génération des simulations
        simulated_lending, simulated_recovery = demonstrate_simulations()
        
        # Démonstration 3: Génération des graphiques
        plot_result = demonstrate_plotting()
        
        # Démonstration 4: Comparaison des méthodes
        mc_result, bs_result = demonstrate_comparison()
        
        print("\n🎉 Démonstration terminée avec succès!")
        print("✅ Toutes les fonctionnalités sont opérationnelles")
        print("\n📝 Prochaines étapes:")
        print("   1. Lancer l'application web (backend + frontend)")
        print("   2. Uploader des fichiers CSV réels")
        print("   3. Lancer une simulation")
        print("   4. Visualiser les trajectoires dans l'interface")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
