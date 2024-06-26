from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class RecoveryForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)
