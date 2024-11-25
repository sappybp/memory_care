from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('ユーザー名は必須です。')
        if not email:
            raise ValueError('メールアドレスは必須です。')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID'
    )
    password = models.CharField(
            max_length=128,
            help_text='パスワードは最低8文字以上必要です。よく使われるパスワードや数字だけのパスワード、あなたの他の個人情報と似ているパスワードは設定できません。',
            verbose_name='パスワード'
    )
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='最終ログイン')
    is_superuser = models.BooleanField(
        default=False,
        help_text='特別な操作なく、このユーザーにすべての権限があることを示します。',
        verbose_name='スーパーユーザー'
    )
    username = models.CharField(
        error_messages={'unique': 'もうすでに存在しているユーザー名です。'},
        help_text='5文字以上50文字以内で、半角英数字と、@/./+/-/_ の記号のみで入力してください。',
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(5,) ,UnicodeUsernameValidator()],
        verbose_name='ユーザーID'
    )
    full_name = models.CharField(blank=True, max_length=50, verbose_name='フルネーム')
    GENDER_CHOICES = (
        (0, '未回答'),
        (1, '男性'),
        (2, '女性'),
        (3, '回答しない'),
    )
    gender = models.IntegerField(default=0, choices=GENDER_CHOICES, verbose_name='性別')
    birth = models.DateField(default=timezone.localdate, verbose_name='生年月日')
    on_work = models.BooleanField(default=False, verbose_name='勤務中')
    CONTRACT_TYPE_CHOICES = (
        (0, '正社員'),
        (1, '契約社員'),
        (2, 'アルバイト'),
        (3, 'パート社員'),
        (4, '派遣社員'),
        (5, 'その他'),
    )
    contract_type = models.IntegerField(default=0, choices=CONTRACT_TYPE_CHOICES, verbose_name='雇用形態')
    AUTHORITY_TYPE_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, 'ユーザー作成削除'),
    )
    authority = models.IntegerField(default=0,choices=AUTHORITY_TYPE_CHOICES, verbose_name='権限')
    email = models.EmailField(max_length=128, unique=True, verbose_name='メールアドレス')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='電話番号')
    introduction = models.TextField(max_length=500, blank=True, null=True, verbose_name='自己紹介')
    is_staff = models.BooleanField(default=False,
        help_text='このユーザーが管理サイトを使用できるかどうかを示します。',
        verbose_name='管理者権限'
    )
    is_active = models.BooleanField(default=True,
        help_text='このユーザーがアクティブかどうかを示します。アカウント削除の代わりにこれを選択解除します。',
        verbose_name='アクティブ'
    )
    date_joined = models.DateTimeField(default=timezone.localtime, verbose_name='登録日')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新日')

    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.full_name
    
    class Meta():
        verbose_name_plural = 'ユーザー情報'

class AttendanceManagement(models.Model):
    user = models.ForeignKey(User, verbose_name='従業員',on_delete=models.PROTECT)
    date = models.DateField(default=timezone.localdate, verbose_name='日付')
    TYPE_CHOICES = (
        (0, '出勤'),
        (1, '退勤'),
    )
    type = models.IntegerField(default=0, choices=TYPE_CHOICES, verbose_name='種類')
    time = models.TimeField(null=True, blank=True, verbose_name='時間')
    biko = models.CharField(max_length=30, default="", null=True, blank=True, verbose_name='備考')
    toroku_date = models.DateTimeField(default=timezone.localtime, verbose_name='登録日')
    update_date = models.DateTimeField(default=timezone.localtime, verbose_name='更新日')

    def __str__(self):
        return self.user.full_name
    
    class Meta():
        verbose_name_plural = '勤怠情報'