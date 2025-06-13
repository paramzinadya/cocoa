from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from cocoahouse import settings


# Create your models here.

class Category(models.Model):
 name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
 slug = models.SlugField(max_length=255, unique=True, db_index=True)

 def __str__(self):
  return self.name

 def get_absolute_url(self):
  return reverse('tag', kwargs={'tag_slug': self.slug})

 class Meta:
  verbose_name = 'Категория'
  verbose_name_plural = 'Категории'

class PublishedModel(models.Manager):
 def get_queryset(self):
  return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)

def translit_to_eng(s: str) -> str:
 d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д':'d','е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и':'i', 'к': 'k','л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п':'p', 'р': 'r','с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х':'h', 'ц': 'c', 'ч': 'ch','ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y','ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}
 return "".join(map(lambda x: d[x] if d.get(x,False) else x, s.lower()))

class Post(models.Model):
 tags = models.ManyToManyField('TagPost', blank=True,related_name='tags')

 class Status(models.IntegerChoices):
  DRAFT = 0, 'Черновик'
  PUBLISHED = 1, 'Опубликовано'

 title = models.CharField(max_length=255,verbose_name="Заголовок")
 slug = models.SlugField(max_length=255, db_index=True, unique=True)
 content = models.TextField(blank=True, verbose_name="Текст статьи")
 time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
 time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
 is_published = models.BooleanField(choices=tuple(map(lambda x:(bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name="Статус")
 objects = models.Manager()
 published = PublishedModel()
 cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts', verbose_name="Категории")
 filial = models.OneToOneField('Filial', on_delete=models.SET_NULL, null=True, blank=True, related_name='Филиал')
 photo = models.FileField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
 author = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, related_name='posts',null=True, default=None)
 likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

 def total_likes(self):
  return self.likes.count()

 class Meta:
  verbose_name = 'Посты'
  verbose_name_plural = 'Посты'
  ordering = ['-time_create']
  indexes = [
   models.Index(fields=['-time_create']),
  ]

 def __str__(self):
  return self.title

 def get_absolute_url(self):
  return reverse('post', kwargs={'post_slug':self.slug})

 def save(self, *args, **kwargs):
  transliterated = translit_to_eng(self.title)
  self.slug = slugify(transliterated)
  super().save(*args, **kwargs)


class Comment(models.Model):
 post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
 author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 body = models.TextField()
 created = models.DateTimeField(auto_now_add=True)

class TagPost(models.Model):
 tag = models.CharField(max_length=100,db_index=True)
 slug = models.SlugField(max_length=255,unique=True)

 def get_absolute_url(self):
  return reverse('tag', kwargs={'tag_slug': self.slug})
 def __str__(self):
  return self.tag

class Filial(models.Model):
  address = models.CharField(max_length=100)
  month = models.IntegerField(null=True)

  def __str__(self):
   return self.address

class UploadFiles(models.Model):
 file = models.FileField(upload_to='uploads_model')