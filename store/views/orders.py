from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from store.middlewares.auth import auth_middleware

class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        total_price = Order.get_total_order_price(customer)
        # Calculate reward points
        reward_points = (total_price // 500) * 10

        # Update customer reward points
        try:
            customer_instance = Customer.objects.get(id=customer)
            customer_instance.reward_points += reward_points
            customer_instance.save()
        except Customer.DoesNotExist:
            # Handle case where customer does not exist
            pass

        print(orders)
        return render(request, 'orders.html', {
            'orders': orders,
            'total_price': total_price,
            'reward_points': reward_points
        })

    def post(self, request):
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            order.cancelled = True  # Marking the order as cancelled
            order.save()
            return redirect('orders')  # Redirect to orders page or wherever appropriate
        except Order.DoesNotExist:
            # Handle case where order does not exist
            return redirect('orders')  # Redirect to orders page or handle error
