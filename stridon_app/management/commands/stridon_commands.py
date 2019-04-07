from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from nucypher_utils.stridon_alice import initialize_alice_policy_pubkey


class Command(BaseCommand):
    # Show this when the user types help
    help = "Create Test Users"

    def handle(self, *args, **options):
        # Initialize alice and policy pubkey
        self.stdout.write("Creating Alice and policy pubkey")
        initialize_alice_policy_pubkey()
        # Create Test Users
        self.stdout.write("Creating test Users")

        try:
            alice = User.objects.get(username='alice')
            self.stdout.write("Alice exists")
        except User.DoesNotExist:
            self.stdout.write("Alice does not exist...creating")
            alice = User.objects.create_user(
                'alice',
                password='stridontest123',
            )

        try:
            free_bob = User.objects.get(username='freebob')
            self.stdout.write("Free Bob exists")
        except User.DoesNotExist:
            self.stdout.write("Free Bob does not exist...creating")
            free_bob = User.objects.create_user(
                'freebob',
                password='stridontest123',
            )

        try:
            paid_bob = User.objects.get(username='paidbob')
            self.stdout.write("Paid Bob exists")
        except User.DoesNotExist:
            self.stdout.write("Paid Bob does not exist...creating")
            paid_bob = User.objects.create_user(
                'paidbob',
                password='stridontest123',
            )

        alice.save()
        free_bob.save()
        paid_bob.save()

        try:
            stridon_admin = User.objects.get(is_superuser=True)
        except User.DoesNotExist:
            self.stdout.write("Please Create a superuser")
            raise

        self.stdout.write("Test Users Created Successfully")

        # Create Groups
        self.stdout.write("Creating Free and Paid Groups")
        free_user_group, created = Group.objects.get_or_create(
            name='Free Users Group',
            )
        paid_user_group, created = Group.objects.get_or_create(
            name='Paid Users Group',
            )

        self.stdout.write("Creating Admin Group")
        admin_user_group, created = Group.objects.get_or_create(
            name='Stridon Admins Group',
        )

        # Fetch the required permission and add it to the group
        self.stdout.write("Adding permissions to Paid Groups")
        can_view_paid_articles_permission = Permission.objects.get(
            codename='can_view_paid_articles',
        )
        paid_user_group.permissions.add(can_view_paid_articles_permission)
        paid_user_group.save()
        free_user_group.save()
        admin_user_group.save()

        # Add users to the groups
        self.stdout.write("Adding users to Free and Paid Groups")
        paid_user_group.user_set.add(alice)
        paid_user_group.save()
        free_user_group.user_set.add(free_bob)
        free_user_group.save()
        paid_user_group.user_set.add(paid_bob)
        paid_user_group.save()
        self.stdout.write("Adding admins to their group")
        admin_user_group.user_set.add(stridon_admin)
        admin_user_group.save()

        # Assert users have permissions
        self.stdout.write("Asserting permissions for each user")
        if alice.has_perm('stridon_app.can_view_paid_articles'):
            self.stdout.write("Alice pass")
        else:
            raise Exception("Permission check failed for Alice")
        if not free_bob.has_perm('stridon_app.can_view_paid_articles'):
            self.stdout.write("Free Bob pass")
        else:
            raise Exception("Permission check failed for Free Bob")
        if paid_bob.has_perm('stridon_app.can_view_paid_articles'):
            self.stdout.write("Paid Bob pass")
        else:
            raise Exception("Permission check failed for Paid Bob")

        # It seems superusers inherit all permissions.

        # if not stridon_admin.has_perm('stridon_app.can_view_paid_articles'):
        #     self.stdout.write("Admin pass")
        # else:
        #     raise Exception("Permission check failed for Admin")
