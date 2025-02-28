from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Prepopulates the database with 15 normal users and 5 admin users'

    def handle(self, *args, **kwargs):
        # Sample names for generating users
        first_names = ['John', 'Jane', 'Alex', 'Mike', 'Linda', 'Chris', 'Sara', 'Tom', 'Kate', 'Nick']
        last_names = ['Smith', 'Doe', 'Brown', 'Johnson', 'Davis', 'Garcia', 'Martinez', 'Clark', 'Lewis', 'Young']

        # Create 15 users
        for i in range(1, 16):
            email = f"user{i}@example.com"
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            password = "password123"
            
            # Create normal user
            CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

        # Create 5 admin users
        for i in range(1, 6):
            email = f"admin{i}@example.com"
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            password = "password123"
            
            CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_admin=True
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 15 normal users and 5 admin users!'))
