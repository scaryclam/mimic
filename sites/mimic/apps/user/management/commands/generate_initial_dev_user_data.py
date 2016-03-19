from django.core.management.base import BaseCommand

from apps.user.services import UserService


class Command(BaseCommand):
    help = "Helper to create initial users after a dev database rebuild"

    def handle(self, *args, **options):
        print "Creating initial user data"
        self.create_users()

    def create_users(self):
        print "Creating users"
        service = UserService()

        users = [
            {'username': 'admin',
             'email': 'admin@example.com',
             'password': 'tester123',
             'is_superuser': True,
             'is_staff': True},
        ]

        for user_data in users:
            print "Creating user %s" % user_data['username']
            user, created = service.create_user(user_data['username'], 
                                                user_data['email'])
            user.is_staff = user_data['is_staff']
            user.is_superuser = user_data['is_superuser']
            user.set_password(user_data['password'])
            user.save()

