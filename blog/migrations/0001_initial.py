# Generated by Django 5.0.4 on 2024-04-13 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('content', models.TextField()),
                ('preview_image', models.ImageField(upload_to='previews/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published', models.BooleanField(default=False)),
                ('views_count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
