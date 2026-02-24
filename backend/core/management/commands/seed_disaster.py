import random
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from core.models import SurvivorCluster, DamageReport

class Command(BaseCommand):
    help = 'Seeds the database with 50 dummy disaster events (survivors, fires, collapsed buildings).'

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing old disaster data...")

        SurvivorCluster.objects.all().delete()
        DamageReport.objects.all().delete()

        center_lat = 18.76
        center_lng = 79.48

        self.stdout.write("Simulating Project Vayu Drishti scan... generating 50 events...")

        for i in range(50):
            lat_offset = random.uniform(-0.05, 0.05)
            lng_offset = random.uniform(-0.05, 0.05)

            lat = center_lat + lat_offset
            lng = center_lng + lng_offset

            location = Point(lng, lat)

            if random.choice([True, False]):
                SurvivorCluster.objects.create(
                    location = location,
                    estimated_count = random.randint(1, 15),
                    radius_meters = round(random.uniform(5.0, 30.0), 2),
                    confidence_score = round(random.uniform(65.0, 98.5), 2),
                    is_rescued = random.choice([True, False, False, False, False])
                )
            else:
                DamageReport.objects.create(
                    location = location,
                    damage_type = random.choice(['FIRE', 'FLOOD', 'COLLAPSE', 'ROAD_BLOCK', 'OTHER']),
                    severity_level = random.choice(['LOW', 'MODERATE', 'HIGH', 'CRITICAL']),
                    description = "Auto generated anamoly detected by Project Vayu-Drishti"
                )

        self.stdout.write("Successfully seeded the database with 50 events")