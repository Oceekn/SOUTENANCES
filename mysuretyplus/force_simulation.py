#!/usr/bin/env python3
"""
Script pour forcer le recalcul d'une simulation
"""

import sys
import os
import django
import threading

# Configuration Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appli_nana.settings')
django.setup()

from simulations.models import Simulation
from simulations.calculations import (
    estimation, 
    calculate_risk_metrics, 
    calculate_real_cumulative
)

def force_simulation_recalculation(simulation_id):
    """Forcer le recalcul d'une simulation"""
    print(f"🔧 Forçage du recalcul de la simulation {simulation_id}")
    print("=" * 50)
    
    try:
        simulation = Simulation.objects.get(id=simulation_id)
        
        print(f"📊 Simulation trouvée:")
        print(f"   ID: {simulation.id}")
        print(f"   Méthode: {simulation.method}")
        print(f"   Échantillons: {simulation.num_samples}")
        print(f"   Status actuel: {simulation.status}")
        
        # Récupérer les DataFrames
        lending_df = simulation.get_lending_dataframe()
        recovery_df = simulation.get_recovery_dataframe()
        
        if lending_df is None or recovery_df is None:
            print("❌ Impossible de charger les DataFrames")
            return False
        
        print(f"✅ DataFrames chargés:")
        print(f"   Lending: {lending_df.shape}")
        print(f"   Recovery: {recovery_df.shape}")
        
        # Forcer le recalcul
        print(f"🚀 Lancement du recalcul...")
        
        # Lancer l'estimation
        provisions_list = estimation(
            lending_df=lending_df,
            recovery_df=recovery_df,
            alpha=simulation.alpha,
            N=simulation.num_samples,
            method=simulation.method
        )
        
        print(f"✅ Estimation terminée - {len(provisions_list)} provisions calculées")
        
        if not provisions_list:
            print("❌ Aucun résultat de simulation")
            return False
        
        # Calculer la provision réelle (premier élément)
        real_provision = provisions_list[0]
        simulated_provisions = provisions_list[1:]  # Exclure la provision réelle
        
        print(f"💰 Provision réelle: {real_provision}")
        print(f"📈 Provisions simulées: {len(simulated_provisions)} valeurs")
        print(f"   Exemples: {simulated_provisions[:5]}")
        
        # Calculer les métriques de risque
        risk_metrics = calculate_risk_metrics(simulated_provisions, simulation.alpha)
        print(f"📊 Métriques de risque calculées")
        
        # Calculer la trajectoire cumulative réelle
        real_cumulative = calculate_real_cumulative(lending_df, recovery_df)
        print(f"📈 Trajectoire réelle calculée - {len(real_cumulative)} points")
        
        # Sauvegarder les résultats
        simulation.real_provision = real_provision
        simulation.set_simulated_provisions_list(simulated_provisions)
        simulation.set_percentiles_dict(risk_metrics['percentiles'])
        simulation.set_confidence_interval_dict(risk_metrics['confidence_interval'])
        simulation.set_real_cumulative_list(real_cumulative)
        simulation.status = 'completed'
        simulation.save()
        
        print(f"✅ Simulation {simulation.id} recalculée avec succès!")
        
        # Vérifier les résultats
        print(f"\n📋 Vérification des résultats:")
        print(f"   Provisions simulées: {len(simulation.get_simulated_provisions_list())}")
        print(f"   Percentiles: {len(simulation.get_percentiles_dict())}")
        print(f"   Intervalle de confiance: {len(simulation.get_confidence_interval_dict())}")
        
        return True
        
    except Simulation.DoesNotExist:
        print(f"❌ Simulation {simulation_id} non trouvée")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du recalcul: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Forçage du recalcul de simulation")
    print()
    
    try:
        simulation_id = input("Entrez l'ID de la simulation à recalculer (ou appuyez sur Entrée pour la plus récente): ").strip()
        
        if not simulation_id:
            # Prendre la simulation la plus récente
            latest_simulation = Simulation.objects.all().order_by('-created_at').first()
            if latest_simulation:
                simulation_id = latest_simulation.id
                print(f"Recalcul de la simulation la plus récente: {simulation_id}")
            else:
                print("❌ Aucune simulation trouvée")
                exit(1)
        
        success = force_simulation_recalculation(int(simulation_id))
        
        if success:
            print("\n🎉 Recalcul terminé avec succès!")
        else:
            print("\n❌ Échec du recalcul")
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
    except ValueError:
        print("❌ ID invalide")
    except Exception as e:
        print(f"❌ Erreur: {e}")

