from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from datetime import datetime


# models
from . models import Company, Product, ProductRequest,\
    TransactionHistory, SalesRecord

# model serializers
from . serializers import CompanySerializer, ProductSerializer, ProductRequestSerializer,\
    TransactionHistorySerializer, SalesRecordSerializer,\
    AllCompanySerializer, AllProductSerializer

# forms
from . forms import UserForm, CompanyForm


# Create your views here.
def registration(request):

    error = ''
    passErrors = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        company_form = CompanyForm(data=request.POST)
        try:
            validate_password(request.POST['password'], user=None, password_validators=None)
            if request.POST['password'] == request.POST['confirm']:
                if user_form.is_valid() and company_form.is_valid():
                    user = user_form.save()
                    user.set_password(user.password)
                    user.save()
                    company = company_form.save(commit=False)
                    company.user = user
                    company.save()
                    return HttpResponseRedirect('/api-auth/login/?next=/')
            else:
                error = 'passwords did\'t match'
        except:
            passErrors = password_validators_help_texts()
    else:
        user_form = UserForm()
        company_form = CompanyForm()

    context_dict = {
        'user_form': user_form,
        'company_form': company_form,
        'error': error,
        'passwordErrors': passErrors,
    }

    return render(request, 'openPW_REST_API/registration.html', context_dict)


class AllCompanyView(viewsets.ModelViewSet):
    serializer_class = AllCompanySerializer
    http_method_names = ['get']

    def get_queryset(self):
        company = Company.objects.all()
        return company


class AllProductView(viewsets.ModelViewSet):
    serializer_class = AllProductSerializer
    http_method_names = ['get']

    def get_queryset(self):
        product = Product.objects.all()
        return product


class CompanyView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace']
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        company = Company.objects.filter(user=user)
        return company


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace']
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        product_set = Product.objects.filter(company__user=user).order_by('-datetime_modified')
        return product_set


class ProductRequestView(viewsets.ModelViewSet):
    serializer_class = ProductRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        productRequest = ProductRequest.objects.filter(company__user=user)
        return productRequest


class TransactionHistoryView(viewsets.ModelViewSet):
    serializer_class = TransactionHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        trans_history = TransactionHistory.objects.filter(company__user=user).order_by('-trans_datetime')
        return trans_history


class SalesRecordView(viewsets.ModelViewSet):
    serializer_class = SalesRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        sales_record = SalesRecord.objects.filter(company__user=user)
        return sales_record


# Http Special Request and Response Cases
class ProductTrans(APIView):
    def record_trans(self, transData, context):
        recordTrans = TransactionHistorySerializer(data=transData, context=context)
        if recordTrans.is_valid():
            recordTrans.save()
            return recordTrans.data

    def check_product_existence(self,  productData):
        try:
            Product.objects.get(company=productData['company'],
                                product_name=productData['product_name'])
            return True
        except Product.DoesNotExist:
            return False

    def put(self, request):
        context = {'request': request}
        product_existence = Product.objects.get(company=request.data['company'],
                                                product_name=request.data['product_name'])
        request.data._mutable = True
        count = int(request.data['product_count']) + product_existence.product_count
        request.data['product_count'] = count
        productModify = ProductSerializer(product_existence, data=request.data, context=context)
        if count < 0:
         return Response('product count should not have a negative value',status=status.HTTP_400_BAD_REQUEST)
        transData = {
            'company': request.data['company'],
            'trans_type': 'modify product',
            'description': 'modify product: ' + request.data['product_name'] + ', count:'
                                        + str(request.data['product_count']) + ' '
                                        + ' with base_price: ' + str(request.data['product_base_price'])
                                        + ' and dispatch_price: ' + str(request.data['product_dispatch_price']),
            'trans_datetime': str(datetime.now()),

        }
        if productModify.is_valid():
            productModify.save()
            self.record_trans(transData, context)
            return Response('product information has been modified', status=status.HTTP_200_OK)
        return Response(productModify.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        context = {'request': request}
        addProduct = ProductSerializer(data=request.data, context=context)

        transData = {
            'company': request.data['company'],
            'trans_type': 'add product',
            'description': 'add product: ' + request.data['product_name'] + ', count:'
                                        + str(request.data['product_count']) + ' '
                                        + ' with base_price: ' + str(request.data['product_base_price'])
                                        + ' and dispatch_price: ' + str(request.data['product_dispatch_price']),
            'trans_datetime': str(datetime.now()),

        }
        checkExistence = self.check_product_existence(request.data)
        if addProduct.is_valid():
            if checkExistence is False:
                addProduct.save()
                self.record_trans(transData, context)
                return Response('product has been added', status=status.HTTP_201_CREATED)
            else:
                return Response('product already exists, do you mean method put?', status=status.HTTP_400_BAD_REQUEST)
        return Response(addProduct.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductTrade(APIView):
#     def post(self, request):
#         context = {'request': request}
#         request.data.is_mutable = False
#         request.data['trans_datetime'] = datetime.now()
#         request.data['is_approved'] = False
#
#         company = Company.objects.get(company_name=request.data['target_company'])
#         requesting_company = Company.objects.get(company_name=request.data['company'])
#
#         tradeData = {
#             'company': company.id,
#             'requesting_company': requesting_company.id,
#             'product': request.data['product'],
#             'target_product': request.data['target_product'],
#             'trans_datetime': datetime.now(),
#             'is_approved': False,
#         }
#
#         requestTrade = ProductExchangeSerializer(data=request.data, context=context)
#         tradeIn = TradeRequestSerializer(data=tradeData, context=context)
#
#         if requestTrade.is_valid() and tradeIn.is_valid():
#             requestTrade.save()
#             tradeIn.save()
#             return Response('trade trans requested', status=status.HTTP_201_CREATED)
#         return Response(requestTrade.errors, status=status.HTTP_400_BAD_REQUEST)
