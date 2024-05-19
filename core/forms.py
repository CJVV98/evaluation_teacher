from django import forms
from user_manage.models import User
from wtforms import Form, StringField, EmailField
from wtforms.validators import DataRequired, Email

class UserForm(forms.Form): 
    user = forms.CharField(label='Username', required=True,widget=forms.TextInput(attrs={'placeholder': 'Usuario'}))
    password = forms.CharField(label='Password', required=True,  widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    class Meta:
        model = User
        fields = ['user', 'password']