from django import forms
from django.utils.deconstruct import deconstructible
from prompt_toolkit.validation import ValidationError

from .models import Category, Filial
from django.core.validators import MinLengthValidator,MaxLengthValidator

@deconstructible
class RussianValidator:
 ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
 code = 'russian'
 def __init__(self, message=None):
  self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."
 def __call__(self, value):
  if not (set(value) <= set(self.ALLOWED_CHARS)):
   raise ValidationError(self.message, code=self.code, params={"value": value})

class AddPostForm(forms.Form):
 title = forms.CharField(max_length=255,
                         min_length=5, label="Заголовок",
                         widget=forms.TextInput(attrs={'class': 'form - input'}),
                         validators = [RussianValidator(),],
                         error_messages = {'min_length': 'Слишком короткий заголовок','required': 'Без заголовка - никак',})
 slug = forms.SlugField(max_length=255, label="URL", validators=[MinLengthValidator(5, message="Минимум 5 символов"), MaxLengthValidator(100, message="Максимум 100 символов"),])
 content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Содержание поста")
 is_published = forms.BooleanField(required=False, label="Опубликовать")
 cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории")
 filial = forms.ModelChoiceField(queryset=Filial.objects.all(), required=False, label="Филиал")

