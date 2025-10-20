from django.urls import path
from .views import (
    SimulationListCreateView,
    SimulationDetailView,
    SimulationStatusView,
    SimulationResultsView,
    RiskCalculationView,
    APIRootView
)

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('simulations/', SimulationListCreateView.as_view(), name='simulation-list-create'),
    path('simulations/<int:pk>/', SimulationDetailView.as_view(), name='simulation-detail'),
    path('simulations/<int:pk>/status/', SimulationStatusView.as_view(), name='simulation-status'),
    path('simulations/<int:pk>/results/', SimulationResultsView.as_view(), name='simulation-results'),
    path('simulations/<int:simulation_id>/calculate_risk/', RiskCalculationView.as_view(), name='risk-calculation'),
]



