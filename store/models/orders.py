from django.db import models
from .product import Products
from .customer import Customer
import datetime


class Order(models.Model):
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField (max_length=50, blank=False)
    phone = models.CharField (max_length=50, blank=False)
    date = models.DateField (default=datetime.datetime.today)
    status = models.BooleanField (default=False)
    cancelled = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

    @staticmethod
    def get_total_order_price(customer_id):
        orders = Order.objects.filter(customer_id=customer_id, status=True)
        return sum(order.price for order in orders)



