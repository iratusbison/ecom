from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from store.middlewares.auth import auth_middleware

class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})
    


    def post(self, request):
        order_id = request.POST.get('order_id')  # Assuming order_id is passed via form
        try:
            order = Order.objects.get(id=order_id)
            order.cancelled = True  # Marking the order as cancelled
            order.save()
            # Optionally, you might want to add a confirmation message or redirect
            return redirect('orders')  # Redirect to orders page or wherever appropriate
        except Order.DoesNotExist:
            # Handle case where order does not exist
            return redirect('orders')  # Redirect to orders page or handle error