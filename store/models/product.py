from django.db import models
from .category import Category, AttributeKey



class AttributeValue(models.Model):
    key = models.ForeignKey(AttributeKey, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key.name}: {self.value}"

class ProductAttribute(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='product_attributes')
    attribute_key = models.ForeignKey(AttributeKey, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_key.name}: {self.attribute_value.value}"

class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/')
    attributes = models.ManyToManyField(AttributeKey, through=ProductAttribute, related_name='products')

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()

    def __str__(self):
        return self.name
        
class ProductImage(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/products/images/')

    def __str__(self):
        return f"{self.product.name} - Image"
