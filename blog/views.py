from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Blog
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'slug', 'content', 'preview_image')
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            slug_name = form.save()
            slug_name.slug = slugify(slug_name.title)
            slug_name.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'slug', 'content', 'preview_image')
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            slug_name = form.save()
            slug_name.slug = slugify(slug_name.title)
            slug_name.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
