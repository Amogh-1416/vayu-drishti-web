from django.contrib.gis.db import models

# Create your models here.
class Drone(models.Model):
    name = models.CharField(max_length=50, unique=True)
    battery_level = models.IntegerField(default=100)

    location = models.PointField(srid=4326, null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class SurvivorCluster(models.Model):
    location = models.PointField(srid=4326)

    estimated_count = models.IntegerField(default=1)

    radius_meters = models.FloatField(default=0.0)

    confidence_score = models.FloatField()

    timestamp = models.DateTimeField(auto_now_add=True)

    is_rescued = models.BooleanField(default=False)

    def __str__(self):
        return f"Cluster of {self.estimated_count} survivors - Confidence: {self.confidence_score}%"
    

class DamageReport(models.Model):
    DAMAGE_TYPES = [
        ('FIRE', 'Fire'),
        ('FLOOD', 'Flood'),
        ('COLLAPSE', 'Collapsed Structure'),
        ('ROAD_BLOCK', 'Blocked Road'),
        ('OTHER', 'Other'),
    ]

    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MODERATE', 'Moderate'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    location = models.PointField(srid=4326)

    damage_type = models.CharField(max_length=20, choices=DAMAGE_TYPES)
    severity_level = models.CharField(max_length=15, choices=SEVERITY_LEVELS)

    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_damage_type_display()} ({self.get_severity_level_display()})"