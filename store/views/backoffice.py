from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from django.contrib.auth.decorators import login_required
from store.models.product import Products
from store.models.orders import Order
from django.http import HttpResponseRedirect
from django.urls import reverse
from .checkout import CheckOut

class BackOffice(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('/admin/login/')  # Redirect non-authenticated or non-admin users to login page

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            orders = Order.objects.filter(date__range=[start_date, end_date])
        else:
            orders = Order.objects.all()  # Get all orders if no date range is specified

        context = {
            'orders': orders,
        }

        return render(request, 'backoffice.html', context)


class CompletedOrders(View):
    def get(self, request):
        completed_orders = Order.objects.filter(status=True, cancelled=False)
        return render(request, 'completed_orders.html', {'orders': completed_orders})

    def post(self, request):
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            if new_status == 'pending':
                order.status = False
                order.cancelled = False
            elif new_status == 'cancelled':
                order.status = False
                order.cancelled = True
            order.save()
        except Order.DoesNotExist:
            pass  # Handle the case where the order does not exist

        # Redirect back to the completed orders page
        return HttpResponseRedirect(reverse('completed_orders'))



class PendingOrders(View):
    def get(self, request):
        pending_orders = Order.objects.filter(status=False, cancelled=False)
        return render(request, 'pending_orders.html', {'orders': pending_orders})

    def post(self, request):
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            if new_status == 'completed':
                order.status = True
                order.cancelled = False
            elif new_status == 'cancelled':
                order.status = False
                order.cancelled = True
            order.save()
        except Order.DoesNotExist:
            pass  # Handle the case where the order does not exist

        # Redirect back to the pending orders page
        return HttpResponseRedirect(reverse('pending_orders'))


class CancelledOrders(View):
    def get(self, request):
        cancelled_orders = Order.objects.filter(cancelled=True)
        return render(request, 'cancelled_orders.html', {'orders': cancelled_orders})

    def post(self, request):
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            if new_status == 'completed':
                order.status = True
                order.cancelled = False
            elif new_status == 'pending':
                order.status = False
                order.cancelled = False
            order.save()
        except Order.DoesNotExist:
            pass  # Handle the case where the order does not exist

        # Redirect back to the cancelled orders page
        return HttpResponseRedirect(reverse('cancelled_orders'))


class CustomerList(View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'customer_list.html', {'customers': customers})

class CustomerDetail(View):
    def get(self, request, customer_id):
        customer = self.get_customer_details(customer_id)
        return render(request, 'customer_detail.html', {'customer': customer})

    def get_customer_details(self, customer_id):
        try:
            return Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return None


class UpdateOrderStatus(View):
    def post(self, request):
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            if new_status == 'completed':
                order.status = True
                order.cancelled = False
            elif new_status == 'pending':
                order.status = False
                order.cancelled = False
            elif new_status == 'cancelled':
                order.status = False
                order.cancelled = True
            order.save()
        except Order.DoesNotExist:
            pass  # Handle the case where the order does not exist

        # Redirect back to the referring page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
