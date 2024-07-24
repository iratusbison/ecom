from django.contrib import admin
from django.urls import path
from .views.home import Index , store, product_detail
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.checkout import CheckOut, UpdateOrderStatus
from .views.orders import OrderView
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('update_order/', UpdateOrderStatus.as_view(), name='update_order'),
    path('orders/cancel/', OrderView.as_view(), name='cancel_order'),
    
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

]
