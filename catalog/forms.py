from django import forms
from catalog.models import Product, Version

forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция",
                   "радар"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'category']
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        data = self.cleaned_data['name']
        for word in forbidden_words:
            if word in data.lower():
                raise forms.ValidationError(f'Использование слова "{word}" в названии продукта недопустимо.')
        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        for word in forbidden_words:
            if word in data.lower():
                raise forms.ValidationError(f'Использование слова "{word}" в названии продукта недопустимо.')
        return data


class VersionForm(forms.ModelForm):
    is_current_version = forms.BooleanField(required=False)

    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_current_version']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('is_current_version') and self.instance and self.instance.pk:
            existing_current_version = Version.objects.filter(is_current_version=True).exclude(
                pk=self.instance.pk).first()
            if existing_current_version:
                existing_current_version.is_current_version = False
                existing_current_version.save()
        return cleaned_data
