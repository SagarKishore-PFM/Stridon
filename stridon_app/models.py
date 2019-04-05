from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# # Create your models here.
# class StridonUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

# @receiver(post_save, sender=User)
# def create_user_stridonuser(sender, instance, created, **kwargs):
#     if created:
#         StridonUser.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_stridonuser(sender, instance, **kwargs):
#     instance.stridonuser.save()

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# TODO:

# (Maybe)
# Add a group model that has FK to user and article.