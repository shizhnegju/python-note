"""
WSGI config for rock project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rock.settings')
sys.path.append('/usr/src/app/rock')
sys.path.append('/usr/src/app/apps')
sys.path.append('/usr/src/app')


application = get_wsgi_application()
