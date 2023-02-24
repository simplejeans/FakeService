from rest_framework import views, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import CreateSchemaSerializer, DatasetSerializer
from .models import Schema, Dataset
from .services import SchemaCreate, start_download_dataset_task
from django.core.cache import cache
from .renderers import PassthroughRenderer
from django.http import FileResponse


class SchemaAPIView(ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = CreateSchemaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = SchemaCreate(data=request.data, user=request.user).create_schema
        return Response(response)

    @action(detail=True, methods=["post"])
    def generate_data(self, request, pk) -> Response:
        count = request.query_params.get("count", 1)
        cache_task_key = start_download_dataset_task(user_id=request.user.id, schema_id=pk, count=count)
        return Response({"Cache task key is": f"{cache_task_key}"}, status=status.HTTP_201_CREATED)


class DataSetView(ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, *args, **kwargs):
        instance = self.get_object()

        file_handle = instance.file.open()

        response = FileResponse(file_handle, content_type='whatever')
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.file.name

        return response


class TaskStatusApiView(views.APIView):

    def get(self, request, format=None):
        task_id = request.query_params['task_id']
        result = cache.get(task_id)
        return Response(result)
