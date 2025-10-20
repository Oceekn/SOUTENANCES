from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Simulation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class SimulationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher les simulations"""
    user = UserSerializer(read_only=True)
    lending_data = serializers.SerializerMethodField()
    recovery_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Simulation
        fields = [
            'id', 'user', 'method', 'num_samples', 'alpha', 
            'created_at', 'completed_at', 'status',
            'lending_file', 'recovery_file', 'real_provision',
            'simulated_provisions', 'percentiles', 'confidence_interval',
            'lending_data', 'recovery_data'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'completed_at', 'status',
            'real_provision', 'simulated_provisions', 'percentiles', 
            'confidence_interval', 'lending_data', 'recovery_data'
        ]
    
    def get_lending_data(self, obj):
        """Retourne un aperçu des données lending"""
        try:
            df = obj.get_lending_dataframe()
            if df is not None:
                return {
                    'shape': df.shape,
                    'columns': df.columns.tolist(),
                    'sample_data': df.head(5).to_dict('records')
                }
            return None
        except:
            return None
    
    def get_recovery_data(self, obj):
        """Retourne un aperçu des données recovery"""
        try:
            df = obj.get_recovery_dataframe()
            if df is not None:
                return {
                    'shape': df.shape,
                    'columns': df.columns.tolist(),
                    'sample_data': df.head(5).to_dict('records')
                }
            return None
        except:
            return None

class SimulationCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer des simulations"""
    
    class Meta:
        model = Simulation
        fields = ['id', 'method', 'num_samples', 'alpha', 'lending_file', 'recovery_file', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
    
    def validate_num_samples(self, value):
        """Valider le nombre d'échantillons"""
        if value < 10:
            raise serializers.ValidationError("Le nombre d'échantillons doit être au moins 10")
        if value > 15000:
            raise serializers.ValidationError("Le nombre d'échantillons ne peut pas dépasser 15,000")
        return value
    
    def validate_method(self, value):
        """Valider la méthode de simulation"""
        if value not in ['montecarlo', 'bootstrap']:
            raise serializers.ValidationError("Méthode invalide. Utilisez 'montecarlo' ou 'bootstrap'")
        return value
    
    def validate_alpha(self, value):
        """Valider le niveau de confiance alpha"""
        if value <= 0 or value >= 1:
            raise serializers.ValidationError("Alpha doit être entre 0 et 1")
        return value
    
    def validate(self, data):
        """Validation globale"""
        lending_file = data.get('lending_file')
        recovery_file = data.get('recovery_file')
        
        if not lending_file:
            raise serializers.ValidationError("Le fichier lending est requis")
        
        if not recovery_file:
            raise serializers.ValidationError("Le fichier recovery est requis")
        
        # Vérifier les extensions des fichiers
        if not lending_file.name.endswith('.csv'):
            raise serializers.ValidationError("Le fichier lending doit être un fichier CSV")
        
        if not recovery_file.name.endswith('.csv'):
            raise serializers.ValidationError("Le fichier recovery doit être un fichier CSV")
        
        return data

class RiskCalculationSerializer(serializers.Serializer):
    """Sérialiseur pour les calculs de risque bidirectionnels"""
    calculation_type = serializers.ChoiceField(
        choices=['risk_to_provision', 'provision_to_risk'],
        help_text="Type de calcul : 'risk_to_provision' ou 'provision_to_risk'"
    )
    risk_level = serializers.FloatField(
        required=False,
        min_value=0.1,
        max_value=99.9,
        help_text="Niveau de risque en pourcentage (pour risk_to_provision)"
    )
    target_provision = serializers.FloatField(
        required=False,
        min_value=0,
        help_text="Montant de la provision cible (pour provision_to_risk)"
    )
    
    def validate(self, data):
        """Validation conditionnelle selon le type de calcul"""
        calculation_type = data.get('calculation_type')
        
        if calculation_type == 'risk_to_provision':
            if 'risk_level' not in data:
                raise serializers.ValidationError("risk_level est requis pour ce type de calcul")
        
        elif calculation_type == 'provision_to_risk':
            if 'target_provision' not in data:
                raise serializers.ValidationError("target_provision est requis pour ce type de calcul")
        
        return data

class SimulationStatusSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le statut des simulations"""
    class Meta:
        model = Simulation
        fields = ['id', 'status', 'created_at', 'completed_at']


