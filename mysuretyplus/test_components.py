#!/usr/bin/env python3
"""
Script de test des composants individuels de l'application
Teste chaque fonction de calcul séparément
"""

import sys
import os
sys.path.append('backend')

def test_calculations():
    """Test des fonctions de calcul"""
    print("🔍 Test des fonctions de calcul...")
    
    try:
        from simulations.calculations import (
            calculer_somme, provision, montecarlo, bootstrap,
            estimation, clean, calculate_risk_metrics
        )
        
        # Test calculer_somme
        print("  ✅ Import des fonctions réussi")
        
        # Créer des données de test
        import pandas as pd
        import numpy as np
        
        # Données de test
        lending_data = {
            'ref_date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'interval': [1, 2, 3],
            'SDATE': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'INTERVAL': [1, 2, 3],
            '50': [5, 3, 2],
            '100': [3, 4, 5],
            '500': [2, 1, 3],
            '1000': [1, 2, 1]
        }
        
        recovery_data = {
            'ref_date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'interval': [1, 2, 3],
            'SDATE': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'INTERVAL': [1, 2, 3],
            '50': [2, 1, 1],
            '100': [1, 2, 3],
            '500': [1, 0, 1],
            '1000': [0, 1, 0]
        }
        
        lending_df = pd.DataFrame(lending_data)
        recovery_df = pd.DataFrame(recovery_data)
        
        print("  ✅ Création des DataFrames de test")
        
        # Test calculer_somme
        try:
            sommes_lending = calculer_somme(lending_df)
            sommes_recovery = calculer_somme(recovery_df)
            print(f"  ✅ calculer_somme - Lending: {sommes_lending}")
            print(f"  ✅ calculer_somme - Recovery: {sommes_recovery}")
        except Exception as e:
            print(f"  ❌ calculer_somme échoué: {e}")
            return False
        
        # Test provision
        try:
            prov, cumulative = provision(lending_df, recovery_df)
            print(f"  ✅ provision - Provision: {prov}")
            print(f"  ✅ provision - Cumulative: {cumulative}")
        except Exception as e:
            print(f"  ❌ provision échoué: {e}")
            return False
        
        # Test montecarlo
        try:
            mc_result = montecarlo(lending_df)
            print(f"  ✅ montecarlo - Shape: {mc_result.shape}")
        except Exception as e:
            print(f"  ❌ montecarlo échoué: {e}")
            return False
        
        # Test bootstrap
        try:
            bs_result = bootstrap(lending_df)
            print(f"  ✅ bootstrap - Shape: {bs_result.shape}")
        except Exception as e:
            print(f"  ❌ bootstrap échoué: {e}")
            return False
        
        # Test estimation
        try:
            est_result = estimation(lending_df, recovery_df, N=10, method="montecarlo")
            print(f"  ✅ estimation - Méthode: {est_result['method']}")
            print(f"  ✅ estimation - Échantillons: {est_result['num_samples']}")
        except Exception as e:
            print(f"  ❌ estimation échoué: {e}")
            return False
        
        # Test clean
        try:
            test_data = [1, 2, 3, 4, 5, 100, 200, 300, 400, 500]
            cleaned = clean(test_data)
            print(f"  ✅ clean - Données nettoyées: {len(cleaned)} éléments")
        except Exception as e:
            print(f"  ❌ clean échoué: {e}")
            return False
        
        # Test calculate_risk_metrics
        try:
            test_provisions = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
            percentiles, confidence_interval = calculate_risk_metrics(test_provisions, 0.95)
            print(f"  ✅ calculate_risk_metrics - Percentiles: {len(percentiles)}")
            print(f"  ✅ calculate_risk_metrics - IC: {confidence_interval}")
        except Exception as e:
            print(f"  ❌ calculate_risk_metrics échoué: {e}")
            return False
        
        print("  ✅ Toutes les fonctions de calcul fonctionnent correctement")
        return True
        
    except ImportError as e:
        print(f"  ❌ Import échoué: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Erreur générale: {e}")
        return False

def test_models():
    """Test des modèles Django"""
    print("\n🔍 Test des modèles Django...")
    
    try:
        # Vérifier que Django est configuré
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appli_nana.settings')
        import django
        django.setup()
        
        from simulations.models import Simulation
        from django.contrib.auth.models import User
        
        print("  ✅ Django configuré et modèles importés")
        
        # Test création d'utilisateur
        try:
            user, created = User.objects.get_or_create(
                username='testuser_models',
                defaults={
                    'email': 'test@example.com',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
            print(f"  ✅ Utilisateur créé/récupéré: {user.username}")
        except Exception as e:
            print(f"  ❌ Création utilisateur échouée: {e}")
            return False
        
        # Test création simulation
        try:
            simulation = Simulation.objects.create(
                user=user,
                method='montecarlo',
                num_samples=100,
                alpha=0.95
            )
            print(f"  ✅ Simulation créée: ID {simulation.id}")
            
            # Test des méthodes du modèle
            simulation.set_simulated_provisions_list([100, 200, 300])
            provisions = simulation.get_simulated_provisions_list()
            print(f"  ✅ Méthodes du modèle: {len(provisions)} provisions")
            
            # Nettoyer
            simulation.delete()
            print("  ✅ Simulation supprimée")
            
        except Exception as e:
            print(f"  ❌ Création simulation échouée: {e}")
            return False
        
        print("  ✅ Tous les modèles fonctionnent correctement")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test des modèles: {e}")
        return False

def test_serializers():
    """Test des sérialiseurs"""
    print("\n🔍 Test des sérialiseurs...")
    
    try:
        from simulations.serializers import (
            SimulationSerializer, SimulationCreateSerializer,
            RiskCalculationSerializer
        )
        
        print("  ✅ Import des sérialiseurs réussi")
        
        # Test SimulationCreateSerializer
        try:
            data = {
                'method': 'montecarlo',
                'num_samples': 100,
                'alpha': 0.95
            }
            serializer = SimulationCreateSerializer(data=data)
            if serializer.is_valid():
                print("  ✅ SimulationCreateSerializer validation réussie")
            else:
                print(f"  ❌ SimulationCreateSerializer validation échouée: {serializer.errors}")
                return False
        except Exception as e:
            print(f"  ❌ Test SimulationCreateSerializer échoué: {e}")
            return False
        
        # Test RiskCalculationSerializer
        try:
            risk_data = {
                'calculation_type': 'risk_to_provision',
                'risk_level': 5.0
            }
            serializer = RiskCalculationSerializer(data=risk_data)
            if serializer.is_valid():
                print("  ✅ RiskCalculationSerializer validation réussie")
            else:
                print(f"  ❌ RiskCalculationSerializer validation échouée: {serializer.errors}")
                return False
        except Exception as e:
            print(f"  ❌ Test RiskCalculationSerializer échoué: {e}")
            return False
        
        print("  ✅ Tous les sérialiseurs fonctionnent correctement")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test des sérialiseurs: {e}")
        return False

def main():
    """Fonction principale de test des composants"""
    print("🚀 TEST DES COMPOSANTS INDIVIDUELS")
    print("=" * 50)
    
    tests = [
        ("Fonctions de calcul", test_calculations),
        ("Modèles Django", test_models),
        ("Sérialiseurs", test_serializers)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  💥 Erreur fatale: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 TOUS LES COMPOSANTS FONCTIONNENT PARFAITEMENT !")
        return True
    else:
        print("⚠️  Certains composants ont des problèmes")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrompus par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Erreur fatale: {e}")
        sys.exit(1)


