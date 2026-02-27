from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurvivorClusterViewSet, DamageReportViewSet

# Router automatically generates the GET, POST, and detail URLs

router = DefaultRouter()
router.register(r'survivors', SurvivorClusterViewSet,basename='survivorcluster')
# use damage-reports so frontend can query /api/damage-reports/?type=...
router.register(r'damage-reports', DamageReportViewSet,basename='damagereport')

urlpatterns = [
    path('', include(router.urls))
]
