from django import forms
from .models import Book, Message


class PictureUpdateForm(forms.ModelForm):
    title = forms.CharField(label = "عنوان", max_length= 100 , required=True)
    edition = forms.IntegerField(label = "ویراست", required=False)
    book_author = forms.CharField(label = "نویسنده", max_length=50)
    publications = forms.CharField(label = "انتشارات", max_length= 50)
    class Meta:
        model = Book
        fields = ['title', 'edition', 'book_author', 'publications', 'content','bookPic']

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class MessageUpdateForm(forms.ModelForm):
    #receiver = forms.CharField(max_length=100)
    #book_post = forms.CharField(max_length=100)
    class Meta:
        model = Message
        fields = [ 'message_title', 'message_content']