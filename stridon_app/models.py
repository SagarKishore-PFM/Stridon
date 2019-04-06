from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(
        User,
        related_name='articles',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ('can_view_paid_articles', 'Can View Paid Articles'),
        ]

# TODO:

# (Maybe)
# Add a group model that has FK to user and article.
