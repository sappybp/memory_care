from django import forms
from .models import Visitor, Dailyreport, Inspection
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            "tsusho_name",
            "tsusho_seinengappi",
            "tsusho_seibetsu",
            "tsusho_phone",
            "tsusho_email",
            "hogo_name",
            "hogo_phone",
            "hogo_email",
            "tokki_naiyo",
        ]
        widgets = {
            'tsusho_seinengappi': forms.SelectDateWidget(
                 empty_label=("選択してください。"),
                 years=range(1900, 2041)
            ),
        }

class DailyreportForm(forms.ModelForm):
    class Meta:
        model = Dailyreport
        fields = [
            "tanto",
            "visitor",
            "tokki_naiyo",
            "tsusho_unagashi",
            "taityomen",
            "haisetsu",
            "kenon_1",
            "kenon_2",
            "chushoku",
            "suibun",
            "sogei_1",
            "sogei_2",
            "shozai_jikan_1",
            "shozai_jikan_2",
            "denwa_shien_1",
            "denwa_shien_2",
            "kesseki",
            "kesseki_kasan",
        ]
        widgets = {
            'shozai_jikan_1': forms.TimeInput(attrs={'type': 'time'}),
            'shozai_jikan_2': forms.TimeInput(attrs={'type': 'time'}),
        }

def contact_form_send_email(request):    
    try:

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email, from_email]

        message = name + ":" + email + "\r\n" + message

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list= recipient_list,
            fail_silently=False
        )

        messages.success(request, 'メールが送信されました。入力したメールアドレスにも同じ内容のメールが送信されます。')
        return redirect('dailyreports:contact_form')
    
    except Exception:

        messages.error(request, 'メール送信に失敗しました。')
        return redirect('dailyreports:contact_form')