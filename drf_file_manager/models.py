import uuid
import hashlib
from pathlib import Path
from datetime import datetime
from functools import partial

import magic
from django.db import models
from django.conf import settings


def md5sum(file, chunksize=4096):
    """calculate the md5 of file
    """
    md5 = hashlib.md5()
    for chunk in iter(partial(file.read, chunksize), b''):
        md5.update(chunk)
    return md5.hexdigest()


def get_upload_to(instance, filename):
    """custom upload_to
    """
    upload_to = getattr(settings, 'FILE_UPLOAD_TO', settings.MEDIA_ROOT)
    name = instance.name.rsplit('.', 1)
    ext = f'.{name[1]}' if len(name) == 2 else ''
    filename = Path(upload_to).joinpath(f'{instance.md5}{ext}')
    return datetime.now().strftime(str(filename))


class FileModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True, verbose_name='文件ID')
    file = models.FileField(
        verbose_name='the file object', upload_to=get_upload_to)
    size = models.IntegerField(
        verbose_name='the filesize',
        editable=False)
    name = models.CharField(
        verbose_name='the filename',
        max_length=50,
        editable=False)
    md5 = models.CharField(
        verbose_name='the md5 of the file',
        unique=True,
        db_index=True,
        max_length=32,
        editable=False)
    created_at = models.DateTimeField(
        verbose_name='the created time of the file',
        auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='the owner of the file',
        null=True,
        on_delete=models.SET_NULL)
    mimetype = models.CharField(
        verbose_name='the mime type of the file',
        max_length=100,
        editable=False)

    def save(self, *args, **kwargs):
        """add informations before save
        """
        md5 = md5sum(self.file)
        self.md5 = md5
        self.size = self.file.size
        self.name = self.file.name
        obj = FileModel.objects.filter(md5=md5).first()
        if not obj:
            self.file.seek(0)
            self.mimetype = magic.from_buffer(self.file.read(4096), mime=True)
            super().save(*args, **kwargs)
        else:
            self.id = obj.id
            self.file = obj.file
            self.mimetype = obj.mimetype
            self.created_at = obj.created_at

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
