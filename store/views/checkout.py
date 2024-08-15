from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from django.contrib.auth.decorators import login_required
from store.models.product import Products
from store.models.orders import Order
from store.models.address import Address
from django.http import HttpResponseRedirect
from django.urls import reverse


class CheckOut(View):
    def get(self, request):
        customer = request.session.get('customer')
        addresses = Address.objects.filter(customer=customer)
        return render(request, 'checkout.html', {'addresses': addresses})

    def post(self, request):
        selected_address = request.POST.get('address')
        address = Address.objects.get(pk=selected_address)
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))

        for product in products:
            order = Order(
                customer=Customer(id=customer),
                product=product,
                price=product.price,
                address=address,  # Link the order to the selected address
                quantity=cart.get(str(product.id))
            )
            order.save()

        request.session['cart'] = {}
        return redirect('cart')

