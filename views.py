from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Message
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from itertools import chain
from .forms import PictureUpdateForm, MessageUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 

# Create your views here.

def home(request):
	context = {
		'books' : Book.objects1.all(),
		'Users' : User.objects.all()
	}
	return render(request, 'shabook/homepage/home.html', context)

def landing(request):
	return render(request, 'shabook/landing.html')

class BookDetailView(DetailView):
    model = Book
    template_name = 'shabook/post_detail.html'
    def dispatch(self, request, *args, **kwargs):
        rhett = super().dispatch(request, args, kwargs)
        request.session['senderr'] = self.get_object().author.username
        request.session['post'] = self.get_object().pk
        return rhett

class BookListView(ListView):
    model = Book
    template_name = 'shabook/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']    #miad be tartibe noozoolie tarikh sort mikone
    paginate_by = 5


class UserBookListView(ListView):
    model = Book
    template_name = 'shabook/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Book.objects1.filter(author=user).order_by('-date_posted')


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    #fields = ['title', 'content', 'date_posted', 'author', 'bookPic']
    form_class = PictureUpdateForm
    template_name = 'shabook/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        image = form.cleaned_data['bookPic']
        form.instance.author = self.request.user
        post.save()
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    #fields = ['title', 'content', 'date_posted', 'author', 'bookPic']
    form_class = PictureUpdateForm
    template_name = 'shabook/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        image = form.cleaned_data['bookPic']
        form.instance.author = self.request.user
        post.save()
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    success_url = '/'

    def test_func(self):  # khob pas in vase ine ke ye vakht bekhaim ye sharte delkhah bedim
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class InboxMessageListView(ListView):
    model = Message
    template_name = 'shabook/my_messages.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'messages'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Message.objects.filter(receiver=user).order_by('-message_date_posted')

class OutboxMessageListView(ListView):
    model = Message
    template_name = 'shabook/my_messages.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'messages'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Message.objects.filter(sender=user).order_by('-message_date_posted')



class MessageDetailView(DetailView):
    model = Message
    def dispatch(self, request, *args, **kwargs):
        rhett = super().dispatch(request, args, kwargs)
        request.session['senderr'] = self.get_object().sender.username
        return rhett

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    # fields = ['title', 'content', 'date_posted', 'author', 'bookPic']
    form_class = MessageUpdateForm
    template_name = 'shabook/message_form.html'

    def form_valid(self, form):
        message = form.save(commit=False)
        form.instance.sender = self.request.user
        b_post =  Book.objects1.get_or_create(pk = self.request.session['post'])[0]
        form.instance.book_post = b_post
        form.instance.receiver = b_post.author
        message.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = '/'

    def test_func(self):  # khob pas in vase ine ke ye vakht bekhaim ye sharte delkhah bedim
        message = self.get_object()
        if self.request.user == message.sender:
            return True
        return False

class MessageReplyView(CreateView):
    model = Message
    # fields = ['title', 'content', 'date_posted', 'author', 'bookPic']
    form_class = MessageUpdateForm
    template_name = 'shabook/message_form.html'

    '''def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)'''

    def form_valid(self, form):

        message = form.save(commit=False)
        form.instance.sender = self.request.user

        b_post = Book.objects1.get_or_create(id=self.kwargs['post'])[0]
        form.instance.book_post = b_post

        #print(type(User.objects.get_or_create(id =self.kwargs['id'])))

        form.instance.receiver = User.objects.get(username = self.request.session['senderr'])
        #print(type(User.objects.get_or_create(id = self.kwargs['id'])))
        #self.request.session['testing'] = "reply"
        message.save()
        return super().form_valid(form)


class SearchView(ListView):
    template_name = 'shabook/view.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            blog_results = Book.objects1.search(query)

            # combine querysets
            queryset_chain = chain(
                blog_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.date_posted,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return Book.objects1.none()  # just an empty queryset as default
