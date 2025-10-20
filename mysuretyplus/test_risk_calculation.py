#!/usr/bin/env python3
"""
Script pour tester les fonctions de calcul de risque
"""

import sys
import os
import django

# Configuration Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appli_nana.settings')
django.setup()

from simulations.models import Simulation
from simulations.calculations import (
    get_provision_for_risk_level, 
    get_risk_level_for_provision
)

def test_risk_calculations(simulation_id):
    """Tester les calculs de risque pour une simulation"""
    print(f"🧪 Test des calculs de risque pour la simulation {simulation_id}")
    print("=" * 60)
    
    try:
        simulation = Simulation.objects.get(id=simulation_id)
        
        # Récupérer les provisions simulées
        provisions = simulation.get_simulated_provisions_list()
        print(f"📊 Provisions disponibles: {len(provisions)} valeurs")
        print(f"   Exemples: {provisions[:5]}")
        
        if not provisions:
            print("❌ Aucune provision disponible")
            return False
        
        # Test 1: Calcul de provision pour un niveau de risque
        print(f"\n🎯 Test 1: Calcul de provision pour risque 5%")
        try:
            provision_5_percent = get_provision_for_risk_level(provisions, 5.0)
            print(f"✅ Provision pour 5% de risque: {provision_5_percent:,.0f} XAF")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
        
        # Test 2: Calcul de provision pour un niveau de risque
        print(f"\n🎯 Test 2: Calcul de provision pour risque 2.5%")
        try:
            provision_2_5_percent = get_provision_for_risk_level(provisions, 2.5)
            print(f"✅ Provision pour 2.5% de risque: {provision_2_5_percent:,.0f} XAF")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
        
        # Test 3: Calcul de risque pour une provision
        print(f"\n🎯 Test 3: Calcul de risque pour provision {provision_5_percent:,.0f}")
        try:
            risk_level = get_risk_level_for_provision(provisions, provision_5_percent)
            print(f"✅ Risque pour {provision_5_percent:,.0f} XAF: {risk_level:.2f}%")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
        
        # Test 4: Calcul de risque pour une provision différente
        test_provision = 260000000  # 260M XAF
        print(f"\n🎯 Test 4: Calcul de risque pour provision {test_provision:,}")
        try:
            risk_level = get_risk_level_for_provision(provisions, test_provision)
            print(f"✅ Risque pour {test_provision:,} XAF: {risk_level:.2f}%")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
        
        print(f"\n🎉 Tous les tests de calcul de risque sont réussis!")
        return True
        
    except Simulation.DoesNotExist:
        print(f"❌ Simulation {simulation_id} non trouvée")
        return False
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Test des fonctions de calcul de risque")
    print()
    
    try:
        simulation_id = input("Entrez l'ID de la simulation à tester (ou appuyez sur Entrée pour la plus récente): ").strip()
        
        if not simulation_id:
            # Prendre la simulation la plus récente
            latest_simulation = Simulation.objects.all().order_by('-created_at').first()
            if latest_simulation:
                simulation_id = latest_simulation.id
                print(f"Test de la simulation la plus récente: {simulation_id}")
            else:
                print("❌ Aucune simulation trouvée")
                exit(1)
        
        success = test_risk_calculations(int(simulation_id))
        
        if success:
            print("\n✅ Les fonctions de calcul de risque fonctionnent correctement!")
        else:
            print("\n❌ Problème avec les fonctions de calcul de risque")
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
    except ValueError:
        print("❌ ID invalide")
    except Exception as e:
        print(f"❌ Erreur: {e}")

