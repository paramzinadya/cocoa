import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model

from cocoa.models import Comment

User = get_user_model()



class LoginUserForm(AuthenticationForm):
 username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class': 'form-input'}))
 password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class': 'forminput'}))
 class Meta:
  model = User
  fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
 username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class': 'form-input'}))
 password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class': 'forminput'}))
 password2 = forms.CharField(label='Повтор пароля',widget=forms.PasswordInput(attrs={'class': 'forminput'}))

 class Meta:
  model = get_user_model()
  fields = ['username', 'email', 'first_name','last_name', 'password', 'password2']
  labels = {
   'email': 'E-mail',
   'first_name': 'Имя',
   'last_name': 'Фамилия',
 }

 def clean_email(self):
  email = self.cleaned_data['email']
  if User.objects.filter(email=email).exists():
   raise forms.ValidationError("Такой E-mail уже существует!")
  return email

class ProfileUserForm(forms.ModelForm):
 username = forms.CharField(disabled=True,label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
 email = forms.CharField(disabled=True, label='Email', widget=forms.TextInput(attrs={'class': 'forminput'}))
 this_year = datetime.date.today().year
 date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5))))
 class Meta:
  model = get_user_model()
  fields = ['photo', 'username', 'email', 'date_birth', 'first_name','last_name']
  labels = {
   'first_name': 'Имя',
   'last_name': 'Фамилия',
 }
 widgets = {
  'first_name':forms.TextInput(attrs={'class': 'form-input'}),
  'last_name':forms.TextInput(attrs={'class': 'form-input'}),
 }
 success_url = reverse_lazy('profile')

 def get_success_url(self):
  return reverse_lazy('profile')

class UserPasswordChangeForm(PasswordChangeForm):
 old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class':'form-input'}))
 new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
 new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'forminput'}))


class CommentForm(forms.ModelForm):
 class Meta:
  model = Comment
  fields = ['body']