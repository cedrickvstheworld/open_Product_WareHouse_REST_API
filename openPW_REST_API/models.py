from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=90, unique=True)
    company_location = models.CharField(max_length=90)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = 'companies'


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=90)
    product_count = models.IntegerField()
    product_base_price = models.FloatField(max_length=30)
    product_dispatch_price = models.FloatField(max_length=30)
    product_description = models.CharField(max_length=128)
    datetime_modified = models.DateTimeField()

    def __str__(self):
        return self.product_name


class ProductRequest(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    requesting_company = models.IntegerField()
    product = models.IntegerField()
    trans_datetime = models.DateTimeField()
    is_approved = models.BooleanField(default=False)


class TransactionHistory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    trans_type = models.CharField(max_length=90)
    description = models.CharField(max_length=128)
    trans_datetime = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'transactionhistories'


class SalesRecord(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    total_expense = models.FloatField(max_length='30', default=None)
    total_sale = models.FloatField(max_length='30', default=None)
    gain = models.FloatField(max_length='30', default=None)
    loss = models.FloatField(max_length='30', default=None)
