from django import forms
from .models import Blog
from django.contrib.auth. forms  import UserCreationForm
from django.contrib.auth. models import User

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['text', 'image']
        
        
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('email','username','password1','password2')
        