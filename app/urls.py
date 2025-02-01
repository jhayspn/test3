from django.urls import path 
from .views import HomePageView, AboutPageView, CakeListView, CakeCreateView,CakeUpdateView,CakeDeleteView, CartOrderView, PaymentPageView, add_cart, update_cart, remove_cart, get_cart, signup, login_view, logout_view
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('cake/', CakeListView.as_view(), name='cake'),
    path('add/', CakeCreateView.as_view(), name='cake_create'),
    path('cake/<int:pk>/edit/', CakeUpdateView.as_view(), name='cake_update'),
    path('cake/<int:pk>/delete/', CakeDeleteView.as_view(), name='cake_delete'),
    path('cart/', CartOrderView.as_view(), name='cart'),
    path('add_cart/<int:post_id>/', add_cart, name='add_cart'),
    path('update_cart/<int:post_id>/', update_cart, name='update_cart'),
    path('remove-cart/<int:post_id>/', remove_cart, name='remove_cart'),
    path('get-cart/', get_cart, name='get_cart'),
    path('process_order/', views.process_order, name='process_order'),
    path('payment/<int:order_id>/', PaymentPageView.as_view(), name='payment'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
]