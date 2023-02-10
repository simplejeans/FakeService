
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import CreateSchemaSerializer
from .models import Schema
from .services import create_schema


class SchemaAPIView(ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = CreateSchemaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_schema(data=request.data, user=request.user)
        return Response(status=status.HTTP_201_CREATED)
