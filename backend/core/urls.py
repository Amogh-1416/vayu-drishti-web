from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurvivorClusterViewSet, DamageReportViewSet

# Router automatically generates the GET, POST, and detail URLs

router = DefaultRouter()
router.register(r'survivors', SurvivorClusterViewSet)
router.register(r'damage', DamageReportViewSet)

urlpatterns = [
    path('', include(router.urls))
]
