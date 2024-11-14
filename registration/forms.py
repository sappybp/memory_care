from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django import forms
from .models import User

User = get_user_model()


subject = "登録確認"
message_template = """
ご登録ありがとうございます。
以下URLをクリックして登録を完了してください。

"""


def get_activate_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return settings.FRONTEND_URL + "activate/{}/{}/".format(uid, token)



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        # 確認するまでログイン不可にする
        user.is_active = False
        
        if commit:
            user.save()
            activate_url = get_activate_url(user)
            message = message_template + activate_url
            # user.email_user(subject, message)
            send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list= [user.email],
                    fail_silently=False
            )
        return user
        

def activate_user(uidb64, token):    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return False

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    
    return False

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "full_name",
            "username",
            "password",
            "birth",
            "gender",
            "phone",
            "email",
            "introduction",
            "on_work",
            "is_active",
            "contract_type",
            "authority",
        ]
        widgets = {
            "birth": forms.SelectDateWidget(
                 empty_label=("選択してください。"),
                 years=range(1900, 2041)
            ),
            "password": forms.PasswordInput(),
        }