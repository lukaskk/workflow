from __future__ import absolute_import, unicode_literals
# Ta linijka zapewnia, że app jest zawsze importowane, gdy Django startuje
from .celery import app as celery_app

__all__ = ('celery_app',)