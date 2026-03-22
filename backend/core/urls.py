from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurvivorClusterViewSet, DamageReportViewSet, handle_video_upload, calculate_route

# Router automatically generates the GET, POST, and detail URLs

router = DefaultRouter()
router.register(r'survivors', SurvivorClusterViewSet)
router.register(r'damage', DamageReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-video/', handle_video_upload, name='upload-video'),
    path('route/', calculate_route, name='calculate-route')
]