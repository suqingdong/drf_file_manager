from pathlib import Path
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import FileModel
from .serializers import FileSerializer
from .utils import get_response


class FileViewSet(viewsets.ModelViewSet):
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        elif self.action in ('destroy',):
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """delete object and file storage
        """
        obj = self.get_object()
        obj.file.delete(save=False)
        obj.delete()
        return Response({'msg': f'the file `{obj.name}` has been deleted.'})
    
    @action(detail=False, methods=['POST'])
    def clean(self, request):
        """delete all files
        """
        for obj in FileModel.objects.all():
            obj.file.delete(save=False)
            obj.delete()
        return Response({'msg': 'all uploaded files have been deleted.'})

    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        """get detail file content
        """
        obj = self.get_object()
        file = Path(obj.file.path)
        if file.exists():
            return get_response(file, request)
        return Response({'error': 'file not exists'})
