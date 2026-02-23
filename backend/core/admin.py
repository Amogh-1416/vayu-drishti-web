from django.contrib.gis import admin
from .models import Drone, SurvivorCluster, DamageReport

# Register your models here.

@admin.register(Drone)
class DroneAdmin(admin.GISModelAdmin):
    list_display = ('name', 'battery_level', 'last_updated')

@admin.register(SurvivorCluster)
class SurvivalClusterAdmin(admin.GISModelAdmin):
    list_display = ('id', 'estimated_count', 'radius_meters', 'is_rescued', 'timestamp')
    list_filter = ('is_rescued',)

@admin.register(DamageReport)
class DamageReportAdmin(admin.GISModelAdmin):
    list_display = ('damage_type', 'severity_level', 'timestamp')
    list_filter = ('damage_type', 'severity_level')
