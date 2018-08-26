from rest_framework import serializers
from . models import Company, Product, ProductRequest,\
      TransactionHistory, SalesRecord
from django.contrib.auth.models import User


class UserPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = User.objects.filter(username=user)
        return queryset


class CompanyPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Company.objects.filter(user=user)
        return queryset


class ProductPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Product.objects.filter(company__user=user)
        return queryset


class allCompanyPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Company.objects.exclude(user=user)
        return queryset


class AllCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class AllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    user = UserPKField()

    class Meta:
        model = Company
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    company = CompanyPKField()

    class Meta:
        model = Product
        fields = '__all__'

class ProductRequestSerializer(serializers.ModelSerializer):
    company = allCompanyPKField()

    class Meta:
        model = ProductRequest
        fields = '__all__'


class TransactionHistorySerializer(serializers.ModelSerializer):
    company = CompanyPKField()

    class Meta:
        model = TransactionHistory
        fields = '__all__'


class SalesRecordSerializer(serializers.ModelSerializer):
    company = CompanyPKField()
    product = ProductPKField()

    class Meta:
        model = SalesRecord
        fields = '__all__'
