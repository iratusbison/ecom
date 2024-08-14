from django.contrib import admin
from django.urls import path
from .views.home import Index , store, product_detail, WishlistView
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.backoffice import UpdateOrderStatus, BackOffice, CustomerList, CustomerDetail, CompletedOrders, PendingOrders, CancelledOrders
from .views.orders import OrderView
from .views.staff_login import StaffLoginView
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store, name='store'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('update_order/', UpdateOrderStatus.as_view(), name='update_order'),
    path('orders/cancel/', OrderView.as_view(), name='cancel_order'),
    path('customers/', CustomerList.as_view(), name='customer_list'),  # URL for customer list
    path('customer/<int:customer_id>/', CustomerDetail.as_view(), name='customer_details'),  # Corrected to point to CustomerDetail
    path('backoffice/', BackOffice.as_view(), name='backoffice'),
    path('completed-orders/', CompletedOrders.as_view(), name='completed_orders'),
    path('pending-orders/', PendingOrders.as_view(), name='pending_orders'),
    path('cancelled-orders/', CancelledOrders.as_view(), name='cancelled_orders'),
    path('staff-login/', StaffLoginView.as_view(), name='staff_login'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),

]