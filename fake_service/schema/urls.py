from rest_framework import routers

from .views import SchemaAPIView

router = routers.DefaultRouter()
router.register(r'schema', SchemaAPIView, basename='schema')

urlpatterns = []

urlpatterns += router.urls
