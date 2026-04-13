"""Comando para crear el superusuario administrador desde variables de entorno."""
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Crea el superusuario si no existe, usando variables de entorno."""

    help = 'Crea el superusuario admin desde variables de entorno (idempotente)'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'El usuario «{username}» ya existe. No se crea de nuevo.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superusuario «{username}» creado correctamente.'))
