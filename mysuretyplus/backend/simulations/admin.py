from django.contrib import admin
from .models import Simulation

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'method', 'num_samples', 'status', 
        'real_provision', 'created_at', 'completed_at'
    ]
    list_filter = ['method', 'status', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = [
        'created_at', 'completed_at', 'real_provision', 
        'simulated_provisions', 'percentiles', 'confidence_interval'
    ]
    
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user',)
        }),
        ('Paramètres de simulation', {
            'fields': ('method', 'num_samples', 'alpha')
        }),
        ('Fichiers', {
            'fields': ('lending_file', 'recovery_file')
        }),
        ('Résultats', {
            'fields': ('status', 'real_provision', 'simulated_provisions', 
                      'percentiles', 'confidence_interval'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
