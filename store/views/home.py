from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from store.models.product import Products
from store.models.category import Category
from django.views import View
from django.http import JsonResponse


class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        # Prepare response data
        new_quantity = cart.get(product, 0)
        return JsonResponse({'success': True, 'new_quantity': new_quantity})

    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


def store(request):

    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}

    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    query = request.GET.get('q')  # Get the search query from the request

    if query:
        products = Products.objects.filter(name__icontains=query)  # Search products by name
    elif categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()

    data = {
        'products': products,
        'categories': categories

    }

    print('you are :', request.session.get('email'))
    return render(request, 'index.html', data)

from collections import defaultdict

from store.models.customer import Customer

def product_detail(request, id):
    product = get_object_or_404(Products, id=id)
    grouped_attributes = defaultdict(list)
    for attribute in product.product_attributes.all():
        grouped_attributes[attribute.attribute_key.name].append(attribute.attribute_value.value)

    message = None

    if request.method == 'POST':
        # Handle Cart Operations
        cart = request.session.get('cart', {})
        product_id = str(product.id)
        action = request.POST.get('action')  # 'add' or 'remove'

        if action == 'add':
            if product_id in cart:
                cart[product_id] += 1
            else:
                cart[product_id] = 1
            message = "Product added to cart."
        elif action == 'remove':
            if product_id in cart and cart[product_id] > 0:
                cart[product_id] -= 1
                if cart[product_id] == 0:
                    del cart[product_id]
            message = "Product removed from cart."
        else:
            message = "Invalid action."

        # Save the updated cart back to the session
        request.session['cart'] = cart

        # Handle Wishlist Operations
        customer_id = request.session.get('customer')
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
                if action == 'add_to_wishlist':
                    if product.id not in customer.wishlist:
                        customer.wishlist.append(product.id)
                        customer.save()
                        message = 'Product added to wishlist.'
                elif action == 'remove_from_wishlist':
                    if product.id in customer.wishlist:
                        customer.wishlist.remove(product.id)
                        customer.save()
                        message = 'Product removed from wishlist.'
                else:
                    message = 'Invalid action.'
            except Customer.DoesNotExist:
                message = 'Customer not found'
        else:
            message = 'Invalid request'

    wishlist_status = product.id in request.session.get('customer_wishlist', [])

    context = {
        'product': product,
        'grouped_attributes': grouped_attributes,
        'wishlist_status': wishlist_status,
        'message': message
    }
    return render(request, 'product_detail.html', context)

from store.models.customer import Customer


from django.shortcuts import redirect

class WishlistView(View):
    def post(self, request):
        customer_id = request.session.get('customer')
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')  # 'add' or 'remove'

        if not customer_id or not product_id:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            customer = Customer.objects.get(id=customer_id)
            product_id = int(product_id)
            if action == 'add':
                if product_id not in customer.wishlist:
                    customer.wishlist.append(product_id)
                    customer.save()
            elif action == 'remove':
                if product_id in customer.wishlist:
                    customer.wishlist.remove(product_id)
                    customer.save()
        except Customer.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Redirect back to the same product detail page
        return redirect(request.META.get('HTTP_REFERER', '/'))


    def get(self, request):
        customer_id = request.session.get('customer')
        if not customer_id:
            return redirect('login')

        try:
            customer = Customer.objects.get(id=customer_id)
            wishlist_products = Products.objects.filter(id__in=customer.wishlist)
            return render(request, 'wishlist.html', {'wishlist_products': wishlist_products})
        except Customer.DoesNotExist:
            return redirect('login')


