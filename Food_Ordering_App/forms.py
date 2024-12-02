from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=255, label='Username',widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':"Obi@1*",}), required=True)
    first_name = forms.CharField(max_length=255, label='First Name',widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':"Ade",}), required=True)
    last_name = forms.CharField(max_length=255, label='Last Name',widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':"Ibro",}), required=True)
    email = forms.CharField(max_length=255, label='Email Address',widget=forms.EmailInput(attrs={'class':"form-control", 'placeholder':"hello@example.com",}), required=True)
    password1 = forms.CharField(max_length=25, label='Password',widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder':"Password",}), required=True)
    password2 = forms.CharField(max_length=25, label='Confirm Password', widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder':"Confirm Password",}), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserProfileForm(forms.Form):
    user_type_choice = [
        ('Driver' , 'DRIVER'),
        ('Customer' , 'CUSTOMER'),
    ]
    profile_image = forms.ImageField(label='Profile Picture',widget=forms.FileInput(attrs={'class':"form-control",}), required=True)
    user_type = forms.ChoiceField(choices=user_type_choice, required=True, label='Account Type',widget=forms.Select(attrs={'class':"form-control"}),)
    phone_number = forms.CharField(max_length=15, label='Phone Number',widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':"+234 900 0000 000",}), required=True)
    

class AddMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = [
            'name',
            'category',
            'price_per_unit',
            'delivery_charge',
            'quantity_available',
            'image',
        ]


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'image',
        ]


from django_recaptcha.fields import ReCaptchaField
class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()
    
    

class UserProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)  # Include any other User fields you want to update
    address = forms.CharField(widget=forms.Textarea())  # Include any other User fields you want to update
    email = forms.EmailField()
    profile_image = forms.ImageField(widget=forms.FileInput(), label="")
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'phone_number', 'address']  # Add other UserProfile fields as necessary

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            # Pre-fill UserProfile fields
            self.fields['profile_image'].initial = user.userprofile.profile_image
            self.fields['phone_number'].initial = user.userprofile.phone_number
