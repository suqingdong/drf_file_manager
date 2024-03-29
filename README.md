# File Manager Application for DjangoRestFramework

## Installation

```bash
python3 -m pip install -U drf_file_manager
```

Windows needs install extra: `python-magic-bin`

```bash
python3 -m pip install python-magic-bin
```

## Usage
1. Add `drf_file_manager` to your `INSTALLED_APPS` setting:

```python
# settings.py
INSTALLED_APPS += [
    'rest_framework',
    'drf_file_manager',
]
```

2. Configuration for `drf_file_manager`:

```python
# settings.py
FILE_UPLOAD_TO = 'data/upload/'
FILE_UPLOAD_MAX_SIZE = '10M'    # [optional]
```

3. Add `drf_file_manager.urls` to your project's urls.py:

```python
# urls.py

urlpatterns += [
    include('api/file/', include('drf_file_manager.urls')),
]
```

## API Endpoints

- `POST /api/file/` - Upload a file
- `GET /api/file/` - List all files
- `GET /api/file/{id}/` - Retrieve a file
- `GET /api/file/{id}/download/` - Download a file (with streaming support)
- `DELETE /api/file/{id}/` - Delete a file
- `POST /api/file/clean/` - Delete all files

#### preview

![](https://suqingdong.github.io/drf_file_manager/src/api-docs.png)