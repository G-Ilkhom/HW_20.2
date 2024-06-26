# Generated by Django 5.0.4 on 2024-04-14 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name': 'blog', 'verbose_name_plural': 'blogs'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='содержимое'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='превью'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='published',
            field=models.BooleanField(default=True, verbose_name='статус публикации'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.CharField(max_length=100, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=100, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='views_count',
            field=models.PositiveIntegerField(default=0, verbose_name='количество просмотров'),
        ),
    ]
