from django.contrib.auth.forms import UserCreationForm, forms
from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'photo', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username','autofocus': 'autofocus'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Password'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Confirm password'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['photo', 'bio', 'password']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
