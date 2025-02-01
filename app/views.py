from django.shortcuts import render
from django.views.generic import TemplateView,ListView, CreateView, UpdateView, DeleteView
from .models import Post, Order, OrderPost
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cake')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cake')
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('cake')

def add_cart(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        cart = request.session.get('cart', {})
        
        add_quantity = int(request.POST.get('quantity', 1))

        if str(post_id) in cart:
            cart[str(post_id)]['quantity'] += add_quantity
        else:
            cart[str(post_id)] = {
                'name': post.name,
                'price': float(post.price),
                'quantity': add_quantity,
            }

        request.session['cart'] = cart
        return redirect('cake')

def update_cart(request, post_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        post = get_object_or_404(Post, id=post_id)
        quantity = int(request.POST.get('quantity', 1))

        if str(post_id) in cart:
            if quantity > 0:
                cart[str(post_id)]['quantity'] = quantity
            else:
                cart.pop(str(post_id), None)
            request.session['cart'] = cart
    return redirect('cart')

def remove_cart(request, post_id):
    cart = request.session.get('cart', {})
    if str(post_id) in cart:
        cart.pop(str(post_id), None)
        request.session['cart'] = cart
    return redirect('cart')

def get_cart(request):
    cart = request.session.get('cart', {})
    return JsonResponse({'cart_posts': list(cart.values())})

def process_order(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')

        order = Order.objects.create()

        for post_id, post in cart.posts(): 
            OrderPost.objects.create(
                ordered=order,
                post_id=post_id,
                quantity=post['quantity'],
                price=post['price']
            )

        request.session['cart'] = {}

        return redirect('order_confirmation', order_id=order.id)
    return redirect('cart')

class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'  

class CakeListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/cake_list.html'     

@method_decorator(login_required, name='dispatch')
class CakeCreateView(CreateView):
    model = Post
    fields = ['name', 'image', 'price']
    template_name = 'app/cake_create.html'
    success_url = reverse_lazy('cake')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CakeUpdateView(UpdateView):
    model = Post
    fields = ['name', 'image', 'price']
    template_name = 'app/cake_update.html'
    success_url = reverse_lazy('cake')

class CakeDeleteView(DeleteView):
    model = Post
    template_name = 'app/cake_delete.html'
    success_url = reverse_lazy('cake')

class CartOrderView(TemplateView):
    template_name = 'app/cart_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})

        for post_id, post in cart.items():
            post['sub_total'] = post['price'] * post['quantity']

        context['cart_posts'] = cart
        context['total_price'] = sum(post['price'] * post['quantity'] for post in cart.values())
        context['posts'] = Post.objects.all()  
        return context

    def post(self, request, *args, **kwargs):
        cart = self.request.session.get('cart', {})
        if not cart:
            return redirect('cart') 

        order = Order.objects.create(
            firstname=request.POST.get('firstname'),
            lastname=request.POST.get('lastname'),
            address=request.POST.get('address'),
            contact=request.POST.get('contact')
        )

        for post_id, post in cart.items():
            OrderPost.objects.create(
                ordered=order,
                post_id=post_id,
                quantity=post['quantity'],
                price=post['price']
            )

        request.session['cart'] = {}
        return redirect('payment', order_id=order.id)

class PaymentPageView(TemplateView):
    template_name = 'app/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        context['order_posts'] = order.items.all()
        
        total_price = 0

        for order_post in context['order_posts']:
            order_post.sub_total = order_post.quantity * order_post.price
            total_price += order_post.sub_total
        context['total_price'] = total_price
        return context