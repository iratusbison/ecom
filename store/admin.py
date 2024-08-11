from django.contrib import admin
from .models.product import Products, ProductAttribute, AttributeValue
from .models.category import Category, AttributeKey
from .models.customer import Customer
from .models.orders import Order

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    inlines = [ProductAttributeInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']



class AttributeKeyAdmin(admin.ModelAdmin):
    list_display = ['name']

class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']

admin.site.register(Products, AdminProduct)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AttributeKey, AttributeKeyAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
admin.site.register(Customer)
admin.site.register(Order)