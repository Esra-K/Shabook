
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from django.db.models import Q

class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(book_author__icontains=query)|
                         Q(content__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class Book(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    book_author = models.CharField(max_length=50)
    edition = models.IntegerField()
    publications = models.CharField(max_length = 50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    bookPic = models.ImageField(default='default.jpg', upload_to='book_pics')
    is_available = models.BooleanField(default = True)
    objects1 = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Message(models.Model):
    message_title = models.CharField(max_length=70)
    message_content = models.TextField()
    message_date_posted = models.DateTimeField(default=timezone.now)
    book_post = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_post')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    def __str__(self):
        return self.message_title

    def get_absolute_url(self):
        return reverse('message-detail', kwargs={'pk': self.pk})

