from django import forms
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

from .models import Category, Filial, Post
from django.core.validators import MinLengthValidator,MaxLengthValidator

def clean_title(self):
 title = self.cleaned_data['title']
 ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
 if not (set(title) <= set(ALLOWED_CHARS)):
     raise ValidationError("Должны быть только русские символы, дефис и пробел.")
 return title


class AddPostForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    filial = forms.ModelChoiceField(queryset=Filial.objects.all(),required=False, empty_label="Нет филиала", label="Филиал")
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'filial', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

class UploadFileForm(forms.Form):
 file = forms.FileField(label="Файл")