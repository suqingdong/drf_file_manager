import os
import mimetypes

from django.http import FileResponse
from rest_framework import status


def file_iterator(file, start=0, length=None):
    """read partial file content"""
    with file.open('rb') as f:
        f.seek(start, os.SEEK_SET)
        content = f.read(length)
        yield content


def get_response(file, request):
    """get file response, support Range request
    """
    file_size = file.stat().st_size
    http_range = request.headers.get('Range') or request.META.get('HTTP_RANGE')

    # get partial content with Range request
    if http_range:
        start, end = http_range.split('=')[-1].split('-')  # Range: =start-end
        start, end = map(int, [start, end])

        end = min([file_size - 1, end])

        content_length = end - start + 1
        content_range = f'bytes {start}-{end}/{file_size}'

        content_type = mimetypes.guess_type(file)[0] or 'application/octet-stream'

        response = FileResponse(file_iterator(file, start=start, length=content_length),
                                status=status.HTTP_206_PARTIAL_CONTENT,
                                content_type=content_type,
                                filename=file.name + '.partial')
        response['Content-Range'] = content_range
        response['Content-Length'] = content_length
    else:
        response = FileResponse(open(file, 'rb'), filename=file.name)
        response['Content-Length'] = file_size

    return response
