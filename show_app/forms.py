from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from show_app.validators import password_form_validator
from show_app.models import SiteUserModel
from django.core.exceptions import ValidationError


class RegisterUserForm(forms.ModelForm):
    password_1 = forms.CharField(label='Пароль', widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password_2 = forms.CharField(label='Пароль повторно',
                                 widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Пароль повторно'}))
    username = forms.CharField(label='Логин', widget=forms.widgets.TextInput(attrs={'placeholder': 'Логин'}))
    email = forms.CharField(label='почта', widget=forms.widgets.EmailInput(attrs={'placeholder': 'Электронная почта'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password_1', 'password_2')

    def clean_email(self):
        '''
        Если почта введеная пользователем уже используется то метод get не выбросит исключения,в таком случае
        возбуждается ValidationError
        '''
        val = self.cleaned_data['email']
        try:
            User.objects.get(email=val)
        except User.DoesNotExist:
            return val
        else:
            raise ValidationError('Эта почта уже используется другим пользователем')

    def clean(self):
        super().clean()
        errors = {}
        print(self.cleaned_data.keys())
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password2 != password1:
            errors['password_1'] = ValidationError('Пароли не совпадают')

        if len(password1) < 8:
            errors['password_1'] = ValidationError('Пароль должен быть не менее восьми символов')

        if errors:
            raise ValidationError(errors)

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.widgets.TextInput(attrs={'placeholder':'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.widgets.PasswordInput(attrs={'placeholder':'Пароль'}))

   




