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
    is_premium_content = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ('can_view_paid_articles', 'Can View Paid Articles'),
        ]

# TODO:

# Try and encrypt the article content that comes as plain text from forms
# and save it into article content field again. See if bytes can be stored in
# TextField. Then decide what to do with the data source pub keys.
