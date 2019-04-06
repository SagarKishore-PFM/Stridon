from django.core.management import BaseCommand

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from ...models import Article


class Command(BaseCommand):
    # Show this when the user types help
    help = "Create Test Users"

    # A command must define handle()
    def handle(self, *args, **options):
        # Create Test Users
        self.stdout.write("Creating test Users")
        alice1, created = User.objects.get_or_create(
            username='alice1',
            email='',
            password='stridontest123',
            )
        alice2, created = User.objects.get_or_create(
            username='alice2',
            email='',
            password='stridontest456',
            )
        alice1.save()
        alice2.save()

        self.stdout.write("Test Users Created Successfully")

        # Create Groups

        self.stdout.write("Creating Free and Paid Groups")


        # free_user_group, created = Group.objects.get_or_create(name='free_users_group')

        # # Get Content for Article Model
        # paid_user_group, created = Group.objects.get_or_create(name='paid_users_group')
        # ct = ContentType.objects.get_for_model(Group)
        # can_view_paid_articles_permission = Permission.objects.create(
        #     codename='can_view_paid_articles',
        #     name='Can view Paid Articles',
        #     content_type=ct)
        # paid_user_group.permissions.add(can_view_paid_articles_permission)



# Add them to groups