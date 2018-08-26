from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('allCompany', views.AllCompanyView, 'allCompany')
router.register('allProduct', views.AllProductView, 'allProduct')
router.register('company', views.CompanyView, 'company')
router.register('productSet', views.ProductView, 'productSet')
router.register('productRequest', views.ProductRequestView, 'productRequest')
router.register('transactionHistory', views.TransactionHistoryView, 'transactionHistory')
router.register('salesRecord', views.SalesRecordView, 'salesRecord')

urlpatterns = [
    path('', include(router.urls)),
    path('index/', views.registration, name='index'),
    path('product_trans/', views.ProductTrans.as_view(), name='product_trans'),
]
