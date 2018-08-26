from .models import Company
from django.contrib.auth.models import User
from django import forms


class Style:
    def __init__(self, x):
        self.tags = x
        self.inputs()

    def inputs(self):
        for i in self.tags:
            htmlclass = {'class': 'form-control-sm', 'placeholder': i[1]}
            i[0].widget.attrs.update(htmlclass)

# forms
class UserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    style = Style([[username, 'Username'], [email, 'Gmail'], [password, 'Password']])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class CompanyForm(forms.ModelForm):
    company_name = forms.CharField()
    company_location = forms.CharField()
    style = Style([[company_name, 'Company Name'], [company_location, 'Location'],])

    class Meta:
        model = Company
        fields = ('company_name', 'company_location',)
