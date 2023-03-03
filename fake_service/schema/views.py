from rest_framework import views, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from schema.serializers import CreateSchemaSerializer, DatasetSerializer
from schema.models import Schema, Dataset
from django.core.cache import cache
from schema.renderers import PassthroughRenderer
from django.http import FileResponse
from schema.tasks import start_generate_data


class SchemaAPIView(ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = CreateSchemaSerializer

    @action(detail=True, methods=["post"], url_name="generate_data")
    def generate_data(self, request, pk) -> Response:
        row_nums = int(request.query_params.get("count", 1))
        cache_task_key = start_generate_data(user_id=request.user.id, schema_id=pk, row_nums=row_nums)
        return Response({"cache_key": cache_task_key}, status=status.HTTP_201_CREATED)


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
