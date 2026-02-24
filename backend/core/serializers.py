from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import SurvivorCluster, DamageReport


class SurvivorClusterSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = SurvivorCluster

        geo_field = "location"

        fields = ['id', 'estimated_count', 'radius_meters', 'confidence_score', 'timestamp', 'is_rescued']


class DamageReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = DamageReport

        geo_field = "location"

        fields = ['id', 'damage_type', 'severity_level', 'description', 'timestamp']