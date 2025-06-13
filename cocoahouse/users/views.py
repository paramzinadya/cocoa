from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from cocoahouse import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
 form_class = AuthenticationForm
 template_name = 'users/login.html'
 extra_context = {'title': "Авторизация"}

 def get_success_url(self):
  return reverse_lazy('home')

def logout_user(request):
 logout(request)
 return HttpResponseRedirect(reverse('users:login'))


def register(request):
 if request.method == 'POST':
  form = RegisterUserForm(request.POST)
  if form.is_valid():
   user = form.save(commit=False)
   user.set_password(form.cleaned_data['password'])  # обязательно хешируем пароль
   user.save()
   login(request, user)  # можно сразу залогинить пользователя после регистрации
   return render(request, 'users/register_done.html', {'user': user})
 else:
  form = RegisterUserForm()
 return render(request, 'users/register.html', {'form': form})

class RegisterUser(CreateView):
 form_class = RegisterUserForm
 template_name = 'users/register.html'
 extra_context = {'title': "Регистрация"}
 success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
 model = get_user_model()
 form_class = ProfileUserForm
 template_name = 'users/profile.html'
 extra_context = {'title': "Профиль пользователя",'default_image': settings.DEFAULT_USER_IMAGE}
 def get_success_url(self):
  return reverse_lazy('users:profile',args=[self.request.user.pk])
 def get_object(self, queryset=None):
  return self.request.user
 success_url = reverse_lazy('profile')


class UserPasswordChange(PasswordChangeView):
 form_class = UserPasswordChangeForm
 success_url = reverse_lazy("users:password_change_done")
 template_name = "users/password_change_form.html"
 extra_context = {'title': "Изменение пароля"}