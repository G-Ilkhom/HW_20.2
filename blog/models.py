from django.db import models

NULL_PARAM = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    slug = models.CharField(max_length=100, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое', **NULL_PARAM)
    preview_image = models.ImageField(upload_to='blog/', verbose_name='превью', **NULL_PARAM)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    published = models.BooleanField(default=True, verbose_name='статус публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f"""{self.title} - {self.slug}, views: {self.views_count}"""

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'
