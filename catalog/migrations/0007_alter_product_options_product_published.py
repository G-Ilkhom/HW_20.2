# Generated by Django 4.2 on 2024-05-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_product_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_cancel_published', 'Can cancel published'), ('can_edit_description', 'Can edit description'), ('can_edit_category', 'Can edit category')], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='product',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
