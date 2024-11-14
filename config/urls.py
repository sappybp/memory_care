from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from django.contrib.auth.models import Group
from registration import views

admin.site.site_title ='日中報告 内部管理サイト'
admin.site.site_header ='日中報告 内部管理サイト'
admin.site.index_title = 'メニュー'
admin.site.unregister(Group)
admin.site.disable_action('delete_selected')

activate_email_sent_view = TemplateView.as_view(template_name="registration/activate_email_sent.html")
index_view = TemplateView.as_view(template_name="registration/index.html")

urlpatterns = [
    path("", index_view, name="index"),
    path("staff_administ/", admin.site.urls),
    path("dailyreports/", include("dailyreports.urls")),
    path("polls/", include("polls.urls")),
    path('', include("django.contrib.auth.urls")),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("activate_email_sent/", activate_email_sent_view, name="activate_email_sent"),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
]
