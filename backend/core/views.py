from django.shortcuts import render
from rest_framework import viewsets
from .models import SurvivorCluster, DamageReport
from .serializers import SurvivorClusterSerializer, DamageReportSerializer

# Create your views here.



# We use ReadOnlyModelViewSet because right now, the frontend map only needs to READ data.
# Drones/Operators will POST data later via WebSockets or a separate endpoint.

class SurvivorClusterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SurvivorClusterSerializer

    def get_queryset(self):
        """Allow filtering by status query parameter.

        - ?status=needs_rescue  -> is_rescued=False
        - ?status=rescued       -> is_rescued=True (optional)
        """
        qs = SurvivorCluster.objects.all()
        status = self.request.query_params.get('status')
        if status:
            if status == 'needs_rescue':
                qs = qs.filter(is_rescued=False)
            elif status == 'rescued':
                qs = qs.filter(is_rescued=True)
        return qs

class DamageReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DamageReportSerializer

    def get_queryset(self):
        """Support filtering by ?type= and/or ?severity=."

        Both parameters may be combined. If none is provided, return all records.
        """
        qs = DamageReport.objects.all()
        t = self.request.query_params.get('type')
        if t:
            qs = qs.filter(damage_type__iexact=t)
        sev = self.request.query_params.get('severity')
        if sev:
            qs = qs.filter(severity_level__iexact=sev)
        return qs
