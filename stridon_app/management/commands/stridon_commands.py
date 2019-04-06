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
        try:
            alice1 = User.objects.get(username='alice1')
            self.stdout.write("Alice1 exists")
        except User.DoesNotExist:
            self.stdout.write("Alice1 does not exist...creating")
            alice1 = User.objects.create_user(
                'alice1',
                password='stridontest123',
            )
        try:
            alice2 = User.objects.get(username='alice2')
            self.stdout.write("Alice2 exists")
        except User.DoesNotExist:
            self.stdout.write("Alice2 does not exist...creating")
            alice2 = User.objects.create_user(
                'alice2',
                password='stridontest123',
            )
        alice1.save()
        alice2.save()

        self.stdout.write("Test Users Created Successfully")

        # Create Groups
        self.stdout.write("Creating Free and Paid Groups")
        free_user_group, created = Group.objects.get_or_create(name='free_users_group')
        paid_user_group, created = Group.objects.get_or_create(name='Paid Users Group')

        # Fetch the required permission and add it to the group
        self.stdout.write("Adding permissions to Paid Groups")
        can_view_paid_articles_permission = Permission.objects.get(
            codename='can_view_paid_articles',
        )
        paid_user_group.permissions.add(can_view_paid_articles_permission)
        paid_user_group.save()
        free_user_group.save()

        # Add users to the groups
        self.stdout.write("Adding users to Free and Paid Groups")
        paid_user_group.user_set.add(alice1)
        free_user_group.user_set.add(alice2)

        # Assert users have permissions
        self.stdout.write("Asserting permissions for each user")
        if alice1.has_perm('stridon_app.can_view_paid_articles'):
            self.stdout.write("Alice 1 pass")
        if not alice2.has_perm('stridon_app.can_view_paid_articles'):
            self.stdout.write("Alice 2 pass")




# Add them to groups