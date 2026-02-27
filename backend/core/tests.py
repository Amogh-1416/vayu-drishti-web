from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point
from .models import SurvivorCluster, DamageReport


class FilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # create survivors
        SurvivorCluster.objects.create(location=Point(0, 0), estimated_count=5, radius_meters=10, confidence_score=80.0, is_rescued=False)
        SurvivorCluster.objects.create(location=Point(1, 1), estimated_count=3, radius_meters=8, confidence_score=75.0, is_rescued=True)

        # damage reports
        DamageReport.objects.create(location=Point(0, 1), damage_type='FIRE', severity_level='CRITICAL', description='burned')
        DamageReport.objects.create(location=Point(1, 0), damage_type='FLOOD', severity_level='LOW', description='wet')
        DamageReport.objects.create(location=Point(2, 2), damage_type='FIRE', severity_level='LOW', description='smoke')

    def test_survivor_status_filter(self):
        # needs_rescue -> only is_rescued=False
        resp = self.client.get('/api/survivors/?status=needs_rescue')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data['features']), 1)
        self.assertFalse(data['features'][0]['properties']['is_rescued'])

        # rescued -> only is_rescued=True
        resp = self.client.get('/api/survivors/?status=rescued')
        data = resp.json()
        self.assertEqual(len(data['features']), 1)
        self.assertTrue(data['features'][0]['properties']['is_rescued'])

    def test_damage_type_and_severity_filters(self):
        # type filter
        resp = self.client.get('/api/damage-reports/?type=FIRE')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # two fire entries
        self.assertEqual(len(data['features']), 2)
        for f in data['features']:
            self.assertEqual(f['properties']['damage_type'], 'FIRE')

        # severity filter
        resp = self.client.get('/api/damage-reports/?severity=CRITICAL')
        data = resp.json()
        self.assertEqual(len(data['features']), 1)
        self.assertEqual(data['features'][0]['properties']['severity_level'], 'CRITICAL')

        # combined type+severity
        resp = self.client.get('/api/damage-reports/?type=FIRE&severity=LOW')
        data = resp.json()
        self.assertEqual(len(data['features']), 1)
        self.assertEqual(data['features'][0]['properties']['damage_type'], 'FIRE')
        self.assertEqual(data['features'][0]['properties']['severity_level'], 'LOW')

