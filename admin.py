from django.contrib import admin
from .models import Book, Message

admin.site.register(Book)

# Register your models here.

admin.site.register(Message)