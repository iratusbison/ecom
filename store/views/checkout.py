from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from django.contrib.auth.decorators import login_required
from store.models.product import Products
from store.models.orders import Order


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')
    
    def get(self, request):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            return redirect('/admin/login/')  # Redirect non-authenticated or non-admin users to login page
        orders = Order.objects.all()  # Get all orders
        customers = Customer.objects.all()  # Get all customers
        return render(request, 'backoffice.html', {'orders': orders, 'customers': customers})



from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse


class UpdateOrderStatus(View):
    def post(self, request):
        order_id = request.POST.get('order_id')
        status = request.POST.get('status') == 'True'  # Convert string to boolean
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
        except Order.DoesNotExist:
            pass  # Handle the case where the order does not exist
        return HttpResponseRedirect(reverse('checkout'))  # Redirect back to the backoffice page
