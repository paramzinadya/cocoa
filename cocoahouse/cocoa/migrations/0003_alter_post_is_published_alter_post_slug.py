# Generated by Django 4.2.1 on 2025-03-25 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocoa', '0002_alter_post_options_post_slug_alter_post_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Опубликовано')], default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
