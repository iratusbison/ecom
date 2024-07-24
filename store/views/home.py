from django.shortcuts import render, redirect, HttpResponseRedirect
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


from django.shortcuts import render, get_object_or_404

def product_detail(request, id):
    product = get_object_or_404(Products, id=id)
    return render(request, 'product_detail.html', {'product': product})