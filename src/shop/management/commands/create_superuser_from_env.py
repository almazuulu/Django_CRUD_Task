from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser using environment variables'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_ADMIN_USERNAME')
        email = os.getenv('DJANGO_ADMIN_EMAIL')
        password = os.getenv('DJANGO_ADMIN_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'All environment variables must be set: '
                'DJANGO_ADMIN_USERNAME, DJANGO_ADMIN_EMAIL, DJANGO_ADMIN_PASSWORD'
            ))
            return

        try:
            # Check whether user is exists
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(
                    f'Superuser {username} created successfully'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Superuser {username} already exists'
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error creating superuser: {str(e)}'
            ))