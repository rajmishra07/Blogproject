from django import forms
from .models import Comment, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }


# Post Form (for creating/editing posts)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your post content'}),
        }


# User Registration Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # Clean username to remove spaces and lowercase it
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if " " in username:
            raise ValidationError("Username cannot contain spaces.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists. Please choose another one.")
        return username

    # Clean email to ensure uniqueness
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists. Please use a different email.")
        return email
