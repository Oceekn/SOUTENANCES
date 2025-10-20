#!/usr/bin/env python3
"""
Script pour vérifier l'état de la simulation dans la base de données
"""

import sys
import os
import django
import json

# Configuration Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appli_nana.settings')
django.setup()

from simulations.models import Simulation

def check_simulation(simulation_id):
    """Vérifier l'état d'une simulation spécifique"""
    print(f"🔍 Vérification de la simulation {simulation_id}")
    print("=" * 50)
    
    try:
        simulation = Simulation.objects.get(id=simulation_id)
        
        print(f"✅ Simulation trouvée:")
        print(f"   ID: {simulation.id}")
        print(f"   Méthode: {simulation.method}")
        print(f"   Échantillons: {simulation.num_samples}")
        print(f"   Alpha: {simulation.alpha}")
        print(f"   Status: {simulation.status}")
        print(f"   Créée le: {simulation.created_at}")
        print(f"   Terminée le: {simulation.completed_at}")
        
        # Vérifier les fichiers
        print(f"\n📁 Fichiers:")
        print(f"   Lending file: {simulation.lending_file.name if simulation.lending_file else 'Aucun'}")
        print(f"   Recovery file: {simulation.recovery_file.name if simulation.recovery_file else 'Aucun'}")
        
        # Vérifier les données
        print(f"\n📊 Données:")
        print(f"   Provision réelle: {simulation.real_provision}")
        
        # Vérifier les provisions simulées
        simulated_provisions = simulation.get_simulated_provisions_list()
        print(f"   Provisions simulées: {len(simulated_provisions)} valeurs")
        if simulated_provisions:
            print(f"   Exemples: {simulated_provisions[:5]}")
        
        # Vérifier les percentiles
        percentiles = simulation.get_percentiles_dict()
        print(f"   Percentiles: {len(percentiles)} clés")
        if percentiles:
            print(f"   Exemples: {dict(list(percentiles.items())[:3])}")
        
        # Vérifier l'intervalle de confiance
        confidence_interval = simulation.get_confidence_interval_dict()
        print(f"   Intervalle de confiance: {len(confidence_interval)} clés")
        if confidence_interval:
            print(f"   Valeurs: {confidence_interval}")
        
        # Vérifier la trajectoire réelle
        real_cumulative = simulation.get_real_cumulative_list()
        print(f"   Trajectoire réelle: {len(real_cumulative)} points")
        if real_cumulative:
            print(f"   Exemples: {real_cumulative[:5]}")
        
        # Vérifier les DataFrames
        print(f"\n📈 DataFrames:")
        lending_df = simulation.get_lending_dataframe()
        recovery_df = simulation.get_recovery_dataframe()
        
        if lending_df is not None:
            print(f"   Lending DataFrame: {lending_df.shape}")
            print(f"   Colonnes: {list(lending_df.columns)}")
        else:
            print(f"   Lending DataFrame: None")
            
        if recovery_df is not None:
            print(f"   Recovery DataFrame: {recovery_df.shape}")
            print(f"   Colonnes: {list(recovery_df.columns)}")
        else:
            print(f"   Recovery DataFrame: None")
        
        return True
        
    except Simulation.DoesNotExist:
        print(f"❌ Simulation {simulation_id} non trouvée")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def list_all_simulations():
    """Lister toutes les simulations"""
    print("📋 Liste de toutes les simulations:")
    print("=" * 50)
    
    simulations = Simulation.objects.all().order_by('-created_at')
    
    if not simulations:
        print("❌ Aucune simulation trouvée")
        return
    
    for sim in simulations:
        print(f"   ID: {sim.id} | Méthode: {sim.method} | Status: {sim.status} | Créée: {sim.created_at}")

if __name__ == "__main__":
    print("🚀 Vérification des simulations dans la base de données")
    print()
    
    # Lister toutes les simulations
    list_all_simulations()
    print()
    
    # Demander l'ID de la simulation à vérifier
    try:
        simulation_id = input("Entrez l'ID de la simulation à vérifier (ou appuyez sur Entrée pour la plus récente): ").strip()
        
        if not simulation_id:
            # Prendre la simulation la plus récente
            latest_simulation = Simulation.objects.all().order_by('-created_at').first()
            if latest_simulation:
                simulation_id = latest_simulation.id
                print(f"Vérification de la simulation la plus récente: {simulation_id}")
            else:
                print("❌ Aucune simulation trouvée")
                exit(1)
        
        check_simulation(int(simulation_id))
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
    except ValueError:
        print("❌ ID invalide")
    except Exception as e:
        print(f"❌ Erreur: {e}")

