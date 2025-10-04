"""WSGI config for batcave_backend project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'batcave_backend.settings')

application = get_wsgi_application()
