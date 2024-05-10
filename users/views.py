import secrets
import string
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from users.models import User
from users.forms import UserRegisterForm
from django.urls import reverse_lazy, reverse
from config.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserPasswordResetView(PasswordResetView):
    template_name = 'recovery_form.html'
    success_url = reverse_lazy('users:login')

    def post(self, request):
        email = request.POST.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user.set_password(new_password)
            user.save()
            send_mail(
                subject="Восстановление пароля",
                message=f"Доброго времени суток!\n"
                        f"Ваш пароль для доступа на сайт AppleStore изменен.\n"
                        f"Данные для входа:\n"
                        f"Email: {email}\n"
                        f"Пароль: {new_password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return HttpResponseRedirect(reverse('users:login'))
        except User.DoesNotExist:
            pass
