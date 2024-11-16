from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone, dateformat
import calendar
import datetime
from django.db.models import F, Q
from django.contrib import messages #　検索結果のメッセージのため追加
from django.contrib.auth.hashers import make_password #パスワードハッシュ化

from registration.models import User, AttendanceManagement
from registration.forms import UserForm
from .models import Visitor, Dailyreport, Inspection
from .forms import VisitorForm, DailyreportForm

#############dailyreport#############
# リスト表示
class DailyreportIndexView(generic.ListView):
    template_name = "dailyreports/dailyreport_index.html"
    context_object_name = "dailyreport_list"
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            queryset = Dailyreport.objects.filter(
                Q(tanto__full_name__icontains=query) |
                Q(visitor__tsusho_name__icontains=query) |
                Q(tokki_naiyo__icontains=query)
            ).order_by("-toroku_date")

            messages.info(self.request, query) #　検索結果メッセージ

        else:
            queryset = Dailyreport.objects.all().order_by("-toroku_date")

        return queryset

# 詳細表示
class DailyreportDetailView(generic.DetailView):
    model = Dailyreport
    template_name = "dailyreports/dailyreport_detail.html"

# 作成
class DailyreportCreateView(generic.FormView):
    template_name = "dailyreports/dailyreport_create_form.html"
    form_class = DailyreportForm

    # tantoの初期値をログインユーザーに設定
    def get_initial(self):
        initial = super().get_initial()
        initial['tanto'] = self.request.user
        return initial

def create_data_dailyreport(request):
    if request.method == 'POST':
        form = DailyreportForm(request.POST)
        if form.is_valid():
            dailyreport = form.save(commit=False)
            # 担当を初期値で入れるようになったため、必要なくなった。
            # dailyreport.tanto = request.user
            dailyreport.save()

            messages.success(request, '日中報告書が作成されました。')
            return redirect('dailyreports:dailyreport_detail', pk=dailyreport.id)
        
        else:
            messages.error(request, '日中報告書を作成できませんでした。')
            return render(request, 'dailyreports/dailyreport_create_form.html', {'form': form})
        
    else:

        messages.error(request, '日中報告書作成への不正なアクセスです。')
        return redirect('dailyreports:dailyreport_index')

# 更新
class DailyreportUpdateView(generic.UpdateView):
    model = Dailyreport
    template_name = "dailyreports/dailyreport_update.html"
    form_class = DailyreportForm

    def get_success_url(self):
        messages.success(self.request, '編集が完了しました。')
        return reverse_lazy("dailyreports:dailyreport_detail", kwargs={'pk': self.object.pk})
# 削除
class DailyreportDeleteView(generic.DeleteView):
    model = Dailyreport

    def get_success_url(self):
        messages.success(self.request, '削除が完了しました。')
        return reverse_lazy("dailyreports:dailyreport_index")

#############dailyreport#############

###############Visitor###############
# リスト表示
class VisitorIndexView(generic.ListView):
    template_name = "dailyreports/visitor_index.html"
    context_object_name = "visitor_list"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            queryset = Visitor.objects.filter(
                Q(tsusho_name__icontains=query) |
                Q(hogo_name__icontains=query) |
                Q(tsusho_phone__icontains=query) |
                Q(tsusho_email__icontains=query) |
                Q(tokki_naiyo__icontains=query)
            ).exclude(is_active=False).order_by('-toroku_date')

            messages.info(self.request, query) #　検索結果メッセージ
        else:

            queryset = Visitor.objects.all().exclude(is_active=False).order_by('-toroku_date')

        return queryset

# 詳細表示
class VisitorDetailView(generic.DetailView):
    model = Visitor
    template_name = "dailyreports/visitor_detail.html"

# 作成
class VisitorCreateView(generic.FormView):
    template_name = "dailyreports/visitor_create_form.html"
    form_class = VisitorForm

def create_data_visitor(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.save()

            messages.success(request, '通所者情報が作成されました。')
            return redirect('dailyreports:visitor_detail', pk=visitor.id)
        
        else:

            messages.error(request, '通所者情報を作成できませんでした。')
            return render(request, 'dailyreports/visitor_create_form.html', {'form': form})
        
    else:

        messages.error(request, '通所者情報作成への不正なアクセスです。')
        return redirect('dailyreports:visitor_index')

# 更新
class VisitorUpdateView(generic.UpdateView):
    model = Visitor
    template_name = "dailyreports/visitor_update.html"
    form_class = VisitorForm

    def get_success_url(self):
        messages.success(self.request, '編集が完了しました。')
        return reverse_lazy("dailyreports:visitor_detail", kwargs={'pk': self.object.pk})
# 削除
class VisitorDeleteView(generic.DeleteView):
    model = Visitor

    def get_success_url(self):
        messages.success(self.request, '削除が完了しました。')
        return reverse_lazy("dailyreports:visitor_index")

# 削除処理
def delete_visitor_data(request, pk):
    try:
        user_id = request.user.id
        control_user = User.objects.get(id=user_id)

        if control_user.authority == 4:

            if Visitor.objects.filter(id=pk).exists():
                
                visitor = Visitor.objects.get(id=pk)

                visitor.is_active = False
                visitor.save()

                messages.success(request, '削除しました。')
                return redirect('dailyreports:visitor_index')
            else:
                messages.error(request, '対象のユーザーが存在しません。')
                return redirect('dailyreports:visitor_index')
        else:
            messages.error(request, '削除権限がありません。')
            return redirect('dailyreports:visitor_index')
    except:
        import sys
        messages.error(request, sys.exc_info())
        # messages.error(request, '削除処理でエラーが発生しました。')
        return redirect('dailyreports:visitor_index')

###############Visitor###############

###############User###############
# リスト表示
class UserIndexView(generic.ListView):
    template_name = "dailyreports/user_index.html"
    context_object_name = "user_list"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            queryset = User.objects.filter(
                Q(username__icontains=query) |
                Q(full_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            ).exclude(is_active=False).order_by('-on_work', '-date_joined')

            messages.info(self.request, query) #　検索結果メッセージ

        else:
            queryset = User.objects.all().exclude(is_active=False).order_by('-on_work', '-date_joined')

        return queryset

# 詳細表示
class UserDetailView(generic.DetailView):
    model = User
    template_name = "dailyreports/user_detail.html"

# 作成
class UserCreateView(generic.FormView):
    template_name = "dailyreports/user_create_form.html"
    form_class = UserForm

def create_data_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #パスワードハッシュ化
            user.password = make_password(user.password)
            user.save()

            messages.success(request, 'ユーザーが作成されました。')
            return redirect('dailyreports:user_detail', pk=user.id)
        
        else:
            messages.error(request, 'ユーザーを作成できませんでした。')
            return render(request, 'dailyreports/user_create_form.html', {'form': form})
        
    else:

        messages.error(request, 'ユーザー作成への不正なアクセスです。')
        return redirect('dailyreports:user_index')
    
def update_on_work(request, pk, on_work):
    try:
        if request.method == 'POST':
            if on_work == 0:
                user = User.objects.get(id=pk)

                time_now=timezone.localtime()
                
                AttendanceManagement.objects.create(
                    user=user,
                    type=0,
                    time=time_now,
                    toroku_date=time_now,
                    update_date=time_now
                )
                user.on_work = True
                user.save()

                messages.success(request, '打刻処理(出勤)が完了しました。')
                return redirect('dailyreports:my_page')

            elif on_work == 1:
                user = User.objects.get(id=pk)

                time_now=timezone.localtime()

                AttendanceManagement.objects.create(
                    user=user,
                    type=1,
                    time=time_now,
                    toroku_date=time_now,
                    update_date=time_now
                )
                user.on_work = False
                user.save()

                messages.success(request, '打刻処理(退勤)が完了しました。')
                return redirect('dailyreports:my_page')

            else:
                messages.error(request, '打刻処理への不正なアクセスです。')
                return redirect('dailyreports:my_page')
                
        else:
            messages.error(request, '打刻処理への不正なアクセスです。')
            return redirect('dailyreports:my_page')
    
    except:
        # import sys
        # messages.error(request, sys.exc_info())
        messages.error(request, '打刻処理に失敗しました。管理者にお問い合わせください。')
        return redirect('dailyreports:my_page')

# 更新
class UserUpdateView(generic.UpdateView):
    model = User
    template_name = "dailyreports/user_update.html"
    form_class = UserForm

    def get_success_url(self):
        messages.success(self.request, '編集が完了しました。')
        return reverse_lazy("dailyreports:user_detail", kwargs={'pk': self.object.pk})

# 削除確認画面表示用
class UserDeleteView(generic.DeleteView):
    model = User
    # template_nameを指定しないとregistration配下を探しに行ってしまうため定義
    template_name = "dailyreports/user_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, '削除が完了しました。')
        return reverse_lazy("dailyreports:user_index")

# 削除処理
def delete_user_data(request, pk):
    try:
        user_id = request.user.id
        control_user = User.object.get(id=user_id)

        if control_user.authority == 4:

            if User.objects.filter(id=pk).exists():
                
                user = User.objects.get(id=pk)

                user.is_active = False
                user.save()

                messages.success(request, '削除しました。')
                return redirect('dailyreports:user_index')
            else:

                messages.error(request, '対象のユーザーが存在しません。')
                return redirect('dailyreports:user_index')
        else:
            
            messages.error(request, '削除権限がありません。')
            return redirect('dailyreports:user_index')
    except:
        # import sys
        # messages.error(request, sys.exc_info())
        messages.error(request, user_id)
        return redirect('dailyreports:user_index')

###############User###############

###############AttendanceManager###############
# リスト表示
class AMIndexView(generic.ListView):
    template_name = "dailyreports/am_index.html"
    context_object_name = "am_list"
    paginate_by = 62

    def get_queryset(self):
        query_user = self.request.user
        query_first_date = self.request.GET.get('query_first_date')
        query_last_date = self.request.GET.get('query_last_date')

        if query_first_date and query_last_date:
            queryset = AttendanceManagement.objects.filter(
                Q(user=query_user),
                Q(date__gte=query_first_date),
                Q(date__lte=query_last_date)
            ).order_by('date')

            messages.info(self.request, query_first_date + "　～　" + query_last_date) #　検索結果メッセージ

        else:
            dt = dateformat.format(timezone.localdate(), 'Y-m')
            query_first_date = dt + "-01"
            query_last_date = str(get_last_date(datetime.date.today()))
            
            queryset = AttendanceManagement.objects.filter(
                Q(user=query_user),
                Q(date__gte=query_first_date),
                Q(date__lte=query_last_date)
            ).order_by('date')

            messages.info(self.request, query_first_date + "　～　" + query_last_date) #　検索結果メッセージ

        return queryset

def get_last_date(dt):
    return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])

def update_am_data(request, pk):
    try:
        if request.method == 'POST':

            if AttendanceManagement.objects.filter(id=pk).exists():
                date = request.POST.get('date')
                type = request.POST.get('type')
                time = request.POST.get('time')
                biko = request.POST.get('biko')
                update_date = timezone.localtime()
                
                am = AttendanceManagement.objects.get(id=pk)
                
                am.date = date
                am.type = type
                am.time = time
                am.biko = biko
                am.update_date = update_date

                am.save()

                messages.success(request, '更新しました。')
                return redirect('dailyreports:am_index')
            else:
                messages.error(request, 'データが存在しないため、更新に失敗しました。')
                return redirect('dailyreports:am_index')
        else:
            raise ValueError
    except:
        # import sys
        # messages.error(request, sys.exc_info())
        messages.error(request, '更新処理への不正なアクセスです。')
        return redirect('dailyreports:am_index')

def delete_am_data(request, pk):
    try:
        if request.method == 'POST':

            if AttendanceManagement.objects.filter(id=pk).exists():
                
                AttendanceManagement.objects.filter(id=pk).delete()

                messages.success(request, '削除しました。')
                return redirect('dailyreports:am_index')
            else:
                messages.error(request, 'データが存在しないため、削除に失敗しました。')
                return redirect('dailyreports:am_index')
        else:
            raise ValueError
    except:
        # import sys
        # messages.error(request, sys.exc_info())
        messages.error(request, '削除処理への不正なアクセスです。')
        return redirect('dailyreports:am_index')

###############AttendanceManager###############

###############my_page###############
# リスト表示
class MyPageView(generic.ListView):
    template_name = "dailyreports/my_page.html"
    context_object_name = "dailyreport_list"
    paginate_by = 5

    def get_queryset(self):

        query_user = self.request.user
        
        queryset = Dailyreport.objects.filter(tanto=query_user).order_by('-toroku_date')[0:20]

        return queryset
###############my_page###############