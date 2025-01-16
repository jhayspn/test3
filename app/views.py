from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Post
from django.urls import reverse_lazy

class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'  

class CakeListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/cake_list.html'     

class CakeDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/cake_detail.html'  

class CakeCreateView(CreateView):
    model = Post
    fields = ['title', 'author', 'body']
    template_name =  'app/cake_create.html'

class CakeUpdateView(UpdateView):
    model = Post
    fields = ['title', 'author', 'body']
    template_name =  'app/cake_update.html'

class CakeDeleteView(DeleteView):
    model = Post
    template_name =  'app/cake_delete.html'
    success_url = reverse_lazy('cake')