from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models.address import Address
from store.models.customer import Customer
from store.forms import AddressForm

def get_logged_in_customer(request):
    customer_id = request.session.get('customer')
    if customer_id:
        return Customer.objects.get(id=customer_id)
    return None

def address_list(request):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect('login')

    addresses = Address.objects.filter(customer=customer)
    return render(request, 'address_list.html', {'addresses': addresses})

def address_add(request):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect('login')

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = customer
            address.save()
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request, 'address_form.html', {'form': form})

def address_edit(request, pk):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect('login')

    address = get_object_or_404(Address, pk=pk, customer=customer)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'address_form.html', {'form': form})

def address_delete(request, pk):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect('login')

    address = get_object_or_404(Address, pk=pk, customer=customer)
    if request.method == 'POST':
        address.delete()
        return redirect('address_list')
    return render(request, 'address_confirm_delete.html', {'address': address})
