from django import forms
from .models import CustomUser,Post,Comments
from django.contrib.auth.forms import UserCreationForm

class CreateUser(forms.Form):
    first_name  = forms.CharField(widget=forms.TextInput(attrs = {"class":"input-area"}))
    phoneNumber = forms.CharField(widget=forms.TextInput(attrs = {"class":"input-area"}))
    username    = forms.CharField(widget=forms.TextInput(attrs = {"class":"input-area"}))
    password    = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input-area"}),required=True)

class Loginform(forms.Form):
    username    = forms.CharField(widget=forms.TextInput(attrs = {"class":"username-area"}))
    password    = forms.CharField(widget=forms.PasswordInput(attrs={"class":"password-area"}),required=True)

class Postform(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 130, "rows": 20, "class": "content-area"}))
    title   = forms.CharField(widget=forms.TextInput(attrs={"class":"title-area"}))
    class Meta:
        model = Post
        fields = ['title','content','type','image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ["comment"]
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'comment-class',  
                'placeholder': 'Enter your comment here...',
                'rows': 4
            }),
        }