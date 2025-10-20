from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import json
import pandas as pd
import os
from django.utils import timezone

class Simulation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('running', 'En cours'),
        ('completed', 'Terminé'),
        ('failed', 'Échoué'),
    ]
    
    METHOD_CHOICES = [
        ('montecarlo', 'Monte Carlo'),
        ('bootstrap', 'Bootstrap'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='montecarlo')
    num_samples = models.IntegerField(default=1000)
    alpha = models.FloatField(default=0.95)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Fichiers uploadés
    lending_file = models.FileField(upload_to='simulations/lending/')
    recovery_file = models.FileField(upload_to='simulations/recovery/')
    
    # Données traitées (stockées en JSON)
    lending_data = models.TextField(blank=True, null=True)
    recovery_data = models.TextField(blank=True, null=True)
    
    # Résultats
    real_provision = models.FloatField(null=True, blank=True)
    simulated_provisions = models.TextField(blank=True, null=True)  # JSON array
    real_cumulative = models.TextField(blank=True, null=True)  # JSON array pour la trajectoire réelle
    percentiles = models.TextField(blank=True, null=True)  # JSON dict
    confidence_interval = models.TextField(blank=True, null=True)  # JSON dict
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Simulation {self.id} - {self.method} - {self.status}"
    
    def get_lending_dataframe(self):
        """Récupère les données lending sous forme de DataFrame"""
        if not self.lending_data:
            return None
        try:
            data = json.loads(self.lending_data)
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Erreur lors de la récupération des données lending: {e}")
            return None
    
    def set_lending_dataframe(self, df):
        """Stocke un DataFrame lending en JSON"""
        if df is not None:
            self.lending_data = df.to_json(orient='records')
        else:
            self.lending_data = None
    
    def get_recovery_dataframe(self):
        """Récupère les données recovery sous forme de DataFrame"""
        if not self.recovery_data:
            return None
        try:
            data = json.loads(self.recovery_data)
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Erreur lors de la récupération des données recovery: {e}")
            return None
    
    def set_recovery_dataframe(self, df):
        """Stocke un DataFrame recovery en JSON"""
        if df is not None:
            self.recovery_data = df.to_json(orient='records')
        else:
            self.recovery_data = None
    
    def get_simulated_provisions_list(self):
        """Récupère la liste des provisions simulées"""
        if not self.simulated_provisions:
            return []
        try:
            return json.loads(self.simulated_provisions)
        except Exception as e:
            print(f"Erreur lors de la récupération des provisions simulées: {e}")
            return []
    
    def set_simulated_provisions_list(self, provisions_list):
        """Stocke la liste des provisions simulées en JSON"""
        if provisions_list is not None:
            self.simulated_provisions = json.dumps(provisions_list)
        else:
            self.simulated_provisions = None
    
    def get_real_cumulative_list(self):
        """Récupère la liste des valeurs cumulatives réelles"""
        if not self.real_cumulative:
            return []
        try:
            return json.loads(self.real_cumulative)
        except Exception as e:
            print(f"Erreur lors de la récupération des valeurs cumulatives réelles: {e}")
            return []
    
    def set_real_cumulative_list(self, cumulative_list):
        """Stocke la liste des valeurs cumulatives réelles en JSON"""
        if cumulative_list is not None:
            self.real_cumulative = json.dumps(cumulative_list)
        else:
            self.real_cumulative = None
    
    
    def get_percentiles_dict(self):
        """Récupère le dictionnaire des percentiles"""
        if not self.percentiles:
            return {}
        try:
            return json.loads(self.percentiles)
        except Exception as e:
            print(f"Erreur lors de la récupération des percentiles: {e}")
            return {}
    
    def set_percentiles_dict(self, percentiles_dict):
        """Stocke le dictionnaire des percentiles en JSON"""
        if percentiles_dict is not None:
            self.percentiles = json.dumps(percentiles_dict)
        else:
            self.percentiles = None
    
    def get_confidence_interval_dict(self):
        """Récupère le dictionnaire de l'intervalle de confiance"""
        if not self.confidence_interval:
            return {}
        try:
            return json.loads(self.confidence_interval)
        except Exception as e:
            print(f"Erreur lors de la récupération de l'intervalle de confiance: {e}")
            return {}
    
    def set_confidence_interval_dict(self, confidence_interval_dict):
        """Stocke le dictionnaire de l'intervalle de confiance en JSON"""
        if confidence_interval_dict is not None:
            self.confidence_interval = json.dumps(confidence_interval_dict)
        else:
            self.confidence_interval = None
    
    def process_uploaded_files(self):
        """Traite les fichiers CSV uploadés et les stocke en JSON"""
        try:
            # Lire le fichier lending
            if self.lending_file:
                lending_df = pd.read_csv(self.lending_file, delimiter=';')
                self.set_lending_dataframe(lending_df)
            
            # Lire le fichier recovery
            if self.recovery_file:
                recovery_df = pd.read_csv(self.recovery_file, delimiter=';')
                self.set_recovery_dataframe(recovery_df)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors du traitement des fichiers: {e}")
            return False
    
    def save(self, *args, **kwargs):
        """Override save pour mettre à jour completed_at si terminé"""
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)
