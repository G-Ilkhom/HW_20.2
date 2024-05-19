from django.db import models
from django.utils.html import mark_safe

from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца продукта", blank=True, null=True, on_delete=models.SET_NULL)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="150" height="150" />' % self.image.url)
        else:
            return "No Image"

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        permissions = [
            ("can_cancel_published", "Can cancel published"),
            ("can_edit_description", "Can edit description"),
            ("can_edit_category", "Can edit category")
        ]


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Version(models.Model):
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="продукт")
    version_number = models.CharField(max_length=50)
    version_name = models.CharField(max_length=100)
    is_current_version = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Версия продукта"
        verbose_name_plural = "Версия продуктов"
        ordering = ["product", "version_name"]

    def __str__(self):
        return f"{self.product} - Version {self.version_number}: {self.version_name}"
