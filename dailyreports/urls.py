from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from . import views, forms

contact_view = TemplateView.as_view(template_name="dailyreports/contact_form.html")

app_name = "dailyreports"
urlpatterns = [
    path("", login_required(views.MyPageView.as_view()), name="my_page"),
    path("dailyreport/", login_required(views.DailyreportIndexView.as_view()), name="dailyreport_index"),
    path("dailyreport/<int:pk>/detail/", login_required(views.DailyreportDetailView.as_view()), name="dailyreport_detail"),
    path("dailyreport/<int:pk>/update/", login_required(views.DailyreportUpdateView.as_view()), name = "dailyreport_update"),
    path("dailyreport/<int:pk>/delete/", login_required(views.DailyreportDeleteView.as_view()), name = "dailyreport_delete"),
    path("dailyreport/create_form/", login_required(views.DailyreportCreateView.as_view()), name="dailyreport_create_form"),
    path("dailyreport/create_data/", login_required(views.create_data_dailyreport), name ="dailyreport_create_data"),
    path("visitor/", login_required(views.VisitorIndexView.as_view()), name="visitor_index"),
    path("visitor/<int:pk>/detail/", login_required(views.VisitorDetailView.as_view()), name="visitor_detail"),
    path("visitor/<int:pk>/update/", login_required(views.VisitorUpdateView.as_view()), name = "visitor_update"),
    path("visitor/<int:pk>/delete_confirm/", login_required(views.VisitorDeleteView.as_view()), name = "visitor_delete_confirm"),
    path("visitor/<int:pk>/delete/", login_required(views.delete_visitor_data), name = "visitor_delete_data"),
    path("visitor/create_form/", login_required(views.VisitorCreateView.as_view()), name="visitor_create_form"),
    path("visitor/create_data/", login_required(views.create_data_visitor), name ="visitor_create_data"),
    path("user/", login_required(views.UserIndexView.as_view()), name="user_index"),
    path("user/<int:pk>/detail/", login_required(views.UserDetailView.as_view()), name="user_detail"),
    path("user/<int:pk>/update/", login_required(views.UserUpdateView.as_view()), name = "user_update"),
    path("user/<int:pk>/delete_confirm/", login_required(views.UserDeleteView.as_view()), name = "user_delete_confirm"),
    path("user/<int:pk>/delete/", login_required(views.delete_user_data), name = "user_delete_data"),
    path("user/create_form/", login_required(views.UserCreateView.as_view()), name="user_create_form"),
    path("user/create_data/", login_required(views.create_data_user), name ="user_create_data"),
    path("user/<int:pk>/<int:on_work>/update_on_work/", login_required(views.update_on_work), name ="update_on_work"),
    path("attendanceManager/", login_required(views.AMIndexView.as_view()), name ="am_index"),
    path("attendanceManager/<int:pk>/update/", login_required(views.update_am_data), name ="update_am_data"),
    path("attendanceManager/<int:pk>/delete/", login_required(views.delete_am_data), name ="delete_am_data"),
    path("contact_form/", login_required(contact_view), name="contact_form"),
    path("contact_send/", login_required(forms.contact_form_send_email), name="contact_send"),
]