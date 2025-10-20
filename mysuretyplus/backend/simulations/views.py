import threading
import time
import json
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

from .models import Simulation
from .serializers import (
    SimulationSerializer, 
    SimulationCreateSerializer, 
    RiskCalculationSerializer,
    SimulationStatusSerializer
)
from .calculations import (
    estimation, 
    calculate_risk_metrics, 
    get_provision_for_risk_level, 
    get_risk_level_for_provision,
    calculate_real_cumulative,
    calculate_simulated_cumulative_trajectories,
    calculate_density_curve,
    generate_trajectory_plot,
    generate_temporal_patterns_plot
)

class SimulationListCreateView(generics.ListCreateAPIView):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Simulation.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        print(f"🔍 SimulationListCreateView - Création d'une nouvelle simulation")
        simulation = serializer.save(user=self.request.user)
        print(f"✅ Simulation créée avec ID: {simulation.id}")
        
        # Traiter les fichiers uploadés
        try:
            print(f"📁 Traitement des fichiers uploadés pour la simulation {simulation.id}")
            simulation.process_uploaded_files()
            simulation.save()
            print(f"✅ Fichiers traités pour la simulation {simulation.id}")
            
            # Lancer la simulation en arrière-plan
            print(f"🚀 Lancement de la simulation {simulation.id} en arrière-plan")
            self._run_simulation_background(simulation)
            
        except Exception as e:
            print(f"❌ Erreur lors du traitement des fichiers pour la simulation {simulation.id}: {e}")
            simulation.status = 'failed'
            simulation.save()
            raise e
    
    def create(self, request, *args, **kwargs):
        """Override create pour retourner la simulation créée"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Retourner la simulation créée avec l'ID
        simulation = Simulation.objects.get(id=serializer.instance.id)
        response_serializer = SimulationSerializer(simulation)
        
        print(f"🔍 SimulationListCreateView - Retour de la simulation {simulation.id}")
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def _run_simulation_background(self, simulation):
        """Lance la simulation en arrière-plan avec une meilleure gestion des erreurs"""
        def run_simulation():
            try:
                print(f"🔍 Début de la simulation {simulation.id}")
                simulation.status = 'running'
                simulation.save()
                
                # Récupérer les DataFrames depuis le modèle
                lending_df = simulation.get_lending_dataframe()
                recovery_df = simulation.get_recovery_dataframe()
                
                print(f"📊 DataFrames récupérés - Lending: {lending_df.shape if lending_df is not None else 'None'}, Recovery: {recovery_df.shape if recovery_df is not None else 'None'}")
                
                if lending_df is None or recovery_df is None:
                    raise Exception("Impossible de charger les données")
                
                # Lancer l'estimation avec la nouvelle logique
                print(f"🚀 Lancement de l'estimation - Méthode: {simulation.method}, Échantillons: {simulation.num_samples}")
                estimation_result = estimation(
                    lending_df=lending_df,
                    recovery_df=recovery_df,
                    alpha=simulation.alpha,
                    N=simulation.num_samples,
                    method=simulation.method
                )
                
                if not estimation_result or 'provisions' not in estimation_result:
                    raise Exception("Aucun résultat de simulation")
                
                provisions_list = estimation_result['provisions']
                print(f"✅ Estimation terminée - {len(provisions_list)} provisions calculées")
                
                # Calculer la provision réelle (premier élément)
                real_provision = provisions_list[0]
                simulated_provisions = provisions_list[1:]  # Exclure la provision réelle
                
                print(f"💰 Provision réelle: {real_provision}")
                print(f"📈 Provisions simulées: {len(simulated_provisions)} valeurs")
                
                # Calculer les métriques de risque
                risk_metrics = calculate_risk_metrics(simulated_provisions, simulation.alpha)
                print(f"📊 Métriques de risque calculées")
                
                # Calculer la trajectoire cumulative réelle
                real_cumulative = calculate_real_cumulative(lending_df, recovery_df)
                print(f"📈 Trajectoire réelle calculée - {len(real_cumulative)} points")
                
                # Générer la courbe de densité selon le code utilisateur
                density_result = calculate_density_curve(simulated_provisions, simulation.method)
                print(f"📊 Courbe de densité générée: {density_result['success'] if density_result else 'Erreur'}")
                
                # Sauvegarder les résultats
                simulation.real_provision = real_provision
                simulation.set_simulated_provisions_list(simulated_provisions)
                simulation.set_percentiles_dict(risk_metrics['percentiles'])
                simulation.set_confidence_interval_dict(risk_metrics['confidence_interval'])
                simulation.set_real_cumulative_list(real_cumulative)
                simulation.status = 'completed'
                simulation.save()
                
                print(f"✅ Simulation {simulation.id} terminée avec succès!")
                
            except Exception as e:
                print(f"❌ Erreur dans la simulation {simulation.id}: {e}")
                import traceback
                traceback.print_exc()
                simulation.status = 'failed'
                simulation.save()
        
        # Lancer dans un thread séparé avec une meilleure gestion
        thread = threading.Thread(target=run_simulation, name=f"Simulation-{simulation.id}")
        thread.daemon = True
        thread.start()
        
        # Attendre un peu pour vérifier que le thread démarre correctement
        time.sleep(0.1)
        if not thread.is_alive():
            print(f"⚠️ Le thread de simulation {simulation.id} n'a pas démarré correctement")
            simulation.status = 'failed'
            simulation.save()

class SimulationDetailView(generics.RetrieveAPIView):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Simulation.objects.filter(user=self.request.user)

class SimulationStatusView(generics.RetrieveAPIView):
    queryset = Simulation.objects.all()
    serializer_class = SimulationStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Simulation.objects.filter(user=self.request.user)

class SimulationResultsView(generics.RetrieveAPIView):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Simulation.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # Filtrer par utilisateur dans retrieve
        simulation_id = kwargs.get('pk')
        try:
            simulation = Simulation.objects.get(id=simulation_id, user=request.user)
        except Simulation.DoesNotExist:
            return Response({'error': 'Simulation non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        
        print(f"🔍 SimulationResultsView - Simulation {simulation.id}")
        print(f"   Status: {simulation.status}")
        
        if simulation.status != 'completed':
            return Response(
                {'error': 'Simulation non terminée'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer les données pour l'affichage
        lending_df = simulation.get_lending_dataframe()
        recovery_df = simulation.get_recovery_dataframe()
        real_cumulative = simulation.get_real_cumulative_list()
        
        # Préparer les données pour les graphiques
        simulated_provisions = simulation.get_simulated_provisions_list()
        percentiles = simulation.get_percentiles_dict()
        confidence_interval = simulation.get_confidence_interval_dict()
        
        print(f"📊 Données récupérées:")
        print(f"   Trajectoire réelle: {len(real_cumulative)} points")
        print(f"   Provisions simulées: {len(simulated_provisions)} valeurs")
        print(f"   Percentiles: {len(percentiles)} clés")
        print(f"   Intervalle de confiance: {len(confidence_interval)} clés")
        
        # Générer les vraies trajectoires simulées avec la même structure que les données originales
        simulated_data = calculate_simulated_cumulative_trajectories(
            lending_df=lending_df,
            recovery_df=recovery_df,
            method=simulation.method,
            num_trajectories=min(10, len(simulated_provisions))  # Limiter à 10 pour l'affichage
        )
        
        simulated_cumulative_data = simulated_data.get('trajectories', [])
        x_axis_values = simulated_data.get('x_axis', [])
        
        print(f"🎯 Vraies trajectoires simulées générées: {len(simulated_cumulative_data)}")
        print(f"📊 Valeurs de l'axe X: {len(x_axis_values)} points")
        if simulated_cumulative_data:
            print(f"   Longueur de la première trajectoire: {len(simulated_cumulative_data[0])}")
            print(f"   Longueur de la trajectoire réelle: {len(real_cumulative)}")
        
        # Générer le graphique des trajectoires
        print(f"🎨 Génération du graphique des trajectoires...")
        trajectory_result = generate_trajectory_plot(
            lending_df=lending_df,
            recovery_df=recovery_df,
            method=simulation.method,
            num_trajectories=min(20, len(simulated_provisions))
        )
        print(f"📊 Graphique des trajectoires généré: {trajectory_result['success'] if trajectory_result else 'Erreur'}")
        
        # Générer la courbe de densité
        print(f"🎨 Génération de la courbe de densité...")
        density_result = calculate_density_curve(simulated_provisions, simulation.method)
        print(f"📊 Courbe de densité générée: {density_result['success'] if density_result else 'Erreur'}")
        
        # Générer les patterns temporels
        print(f"🎨 Génération des patterns temporels...")
        patterns_result = generate_temporal_patterns_plot(
            lending_df=lending_df,
            recovery_df=recovery_df,
            simulated_lending_list=[],  # Sera généré dans la fonction
            simulated_recovery_list=[],  # Sera généré dans la fonction
            method=simulation.method,
            num_samples=min(20, simulation.num_samples)
        )
        print(f"📊 Patterns temporels générés: {patterns_result['success'] if patterns_result else 'Erreur'}")
        
        response_data = {
            'id': simulation.id,
            'method': simulation.method,
            'num_samples': simulation.num_samples,
            'alpha': simulation.alpha,
            'real_provision': simulation.real_provision,
            'real_cumulative': real_cumulative,
            'simulated_provisions': simulated_provisions,  # Garder toutes les provisions
            'simulated_cumulative': simulated_cumulative_data,
            'x_axis_values': x_axis_values,  # Valeurs spécifiques pour l'axe X des graphiques
            'percentiles': percentiles,
            'confidence_interval': confidence_interval,
            'trajectory_plot': {
                'image_base64': trajectory_result.get('image_base64', '') if trajectory_result else '',
                'success': trajectory_result.get('success', False) if trajectory_result else False,
                'stats': trajectory_result.get('stats', {}) if trajectory_result else {}
            },
            'density_curve': {
                'image_base64': density_result.get('image_base64', '') if density_result else '',
                'success': density_result.get('success', False) if density_result else False
            },
            'patterns_plot': {
                'image_base64': patterns_result.get('image_base64', '') if patterns_result else '',
                'success': patterns_result.get('success', False) if patterns_result else False,
                'method': patterns_result.get('method', simulation.method) if patterns_result else simulation.method,
                'num_samples': patterns_result.get('num_samples', min(20, simulation.num_samples)) if patterns_result else min(20, simulation.num_samples),
                'simulations_shown': patterns_result.get('simulations_shown', 0) if patterns_result else 0
            },
            'status': simulation.status,
            'created_at': simulation.created_at,
            'completed_at': simulation.completed_at
        }
        
        print(f"✅ Données envoyées au frontend:")
        print(f"   ID: {response_data['id']}")
        print(f"   Méthode: {response_data['method']}")
        print(f"   Provisions simulées: {len(response_data['simulated_provisions'])}")
        print(f"   Courbe de densité: {'Oui' if response_data['density_curve']['image_base64'] else 'Non'}")
        print(f"   Taille image base64: {len(response_data['density_curve']['image_base64']) if response_data['density_curve']['image_base64'] else 0} caractères")
        print(f"   Trajectoires simulées: {len(response_data['simulated_cumulative'])}")
        
        return Response(response_data)

class RiskCalculationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, simulation_id):
        print(f"🔍 RiskCalculationView - Calcul pour simulation {simulation_id}")
        print(f"   Données reçues: {request.data}")
        
        serializer = RiskCalculationSerializer(data=request.data)
        if serializer.is_valid():
            calculation_type = serializer.validated_data['calculation_type']
            print(f"   Type de calcul: {calculation_type}")
            
            # Récupérer la simulation spécifique
            try:
                simulation = Simulation.objects.get(
                    id=simulation_id,
                    user=request.user, 
                    status='completed'
                )
                print(f"✅ Simulation trouvée: {simulation.id}")
            except Simulation.DoesNotExist:
                print(f"❌ Simulation {simulation_id} non trouvée")
                return Response(
                    {'error': 'Simulation non trouvée ou non terminée'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            provisions = simulation.get_simulated_provisions_list()
            print(f"📊 Provisions récupérées: {len(provisions)} valeurs")
            print(f"   Exemples: {provisions[:5]}")
            
            if not provisions:
                print(f"❌ Aucune provision disponible")
                return Response(
                    {'error': 'Aucune donnée de simulation disponible'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if calculation_type == 'risk_to_provision':
                risk_level = serializer.validated_data['risk_level']
                print(f"🎯 Calcul provision pour risque {risk_level}%")
                provision_value = get_provision_for_risk_level(provisions, risk_level)
                print(f"💰 Provision calculée: {provision_value}")
                
                result = {
                    'risk_level': risk_level,
                    'provision_value': provision_value,
                    'method': simulation.method
                }
                print(f"✅ Résultat envoyé: {result}")
                return Response(result)
            
            elif calculation_type == 'provision_to_risk':
                target_provision = serializer.validated_data['target_provision']
                print(f"🎯 Calcul risque pour provision {target_provision}")
                risk_level = get_risk_level_for_provision(provisions, target_provision)
                print(f"⚠️ Risque calculé: {risk_level}%")
                
                result = {
                    'target_provision': target_provision,
                    'risk_level': risk_level,
                    'method': simulation.method
                }
                print(f"✅ Résultat envoyé: {result}")
                return Response(result)
            else:
                print(f"❌ Type de calcul inconnu: {calculation_type}")
        
        print(f"❌ Erreurs de validation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APIRootView(APIView):
    def get(self, request):
        return Response({
            'message': 'API d\'évaluation du risque de crédit',
            'endpoints': {
                'simulations': '/api/simulations/',
                'simulation_status': '/api/simulations/{id}/status/',
                'simulation_results': '/api/simulations/{id}/results/',
                'risk_calculation': '/api/risk-calculation/',
            }
        })
