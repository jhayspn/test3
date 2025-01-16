from django.urls import path 
from .views import HomePageView, AboutPageView,CakeListView,CakeDetailView,CakeCreateView,CakeUpdateView,CakeDeleteView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('cake/', CakeListView.as_view(), name='cake'),
    path('cake/<int:pk>', CakeDetailView.as_view(), name='cake_detail'),
    path('cake/create', CakeCreateView.as_view(), name='cake_create'),
    path('cake/<int:pk>/edit', CakeUpdateView.as_view(), name='cake_update'),
    path('cake/<int:pk>/delete', CakeDeleteView.as_view(), name='cake_delete'),
]