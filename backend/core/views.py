from django.shortcuts import render
from rest_framework import viewsets
from .models import SurvivorCluster, DamageReport
from .serializers import SurvivorClusterSerializer, DamageReportSerializer

# Create your views here.



# We use ReadOnlyModelViewSet because right now, the frontend map only needs to READ data.
# Drones/Operators will POST data later via WebSockets or a separate endpoint.

class SurvivorClusterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SurvivorCluster.objects.all()
    serializer_class = SurvivorClusterSerializer

class DamageReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DamageReport.objects.all()
    serializer_class = DamageReportSerializer
