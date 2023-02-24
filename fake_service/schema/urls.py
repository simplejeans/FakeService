from rest_framework import routers
from .views import SchemaAPIView, DataSetView, TaskStatusApiView
from django.urls import path

router = routers.DefaultRouter()

router.register(r"schema", SchemaAPIView, basename="schema")
router.register(r"dataset", DataSetView, basename="dataset")

urlpatterns = [
    path('task_status/', TaskStatusApiView.as_view(), )
]

urlpatterns += router.urls
