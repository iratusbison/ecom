from django.shortcuts import render, redirect
from django.views import View
from store.models.orders import Order
from store.models.product import Products

class Cart(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        ids = list(cart.keys())
        products = Products.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products})

    def post(self, request):
        product_id = request.POST.get('product')
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if product_id in cart:
            if action == 'remove':
                if cart[product_id] > 1:
                    cart[product_id] -= 1
                else:
                    del cart[product_id]
            elif action == 'add':
                cart[product_id] += 1
        else:
            if action == 'add':
                cart[product_id] = 1

        request.session['cart'] = cart
        return redirect('cart')
    

