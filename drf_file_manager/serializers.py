from pathlib import Path
import humanfriendly

from django.conf import settings
from rest_framework import serializers
from .models import FileModel


class FileSerializer(serializers.ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file_path = serializers.SerializerMethodField()
    file_uri = serializers.SerializerMethodField()

    class Meta:
        model = FileModel
        fields = '__all__'

    def validate_file(self, data):
        max_size = getattr(settings, 'FILE_UPLOAD_MAX_SIZE', None)
        if max_size and data.size > humanfriendly.parse_size(str(max_size)):
            raise serializers.ValidationError(f'file size limit {max_size}')
        return data

    def get_file_path(self, obj):
        return Path(obj.file.path).as_posix().replace(settings.BASE_DIR.as_posix() + '/', '')

    def get_file_uri(self, obj):
        prefix = getattr(settings, 'FILE_URI_PREFIX', 'api/file/')
        return f'/{prefix}{obj.id}/download/'
