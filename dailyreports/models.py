from django.db import models
from django.utils import timezone

from registration.models import User

# 通所者情報
class Visitor(models.Model):
    tsusho_name = models.CharField(max_length=30, verbose_name='通所者氏名')
    tsusho_seinengappi= models.DateField(verbose_name='通所者生年月日')
    SEIBETSU_CHOICES = (
        (0, "未回答"),
        (1, '男性'),
        (2, '女性'),
        (3, '回答しない'),
    )
    tsusho_seibetsu = models.IntegerField(default=0, choices=SEIBETSU_CHOICES, verbose_name='通所者性別')
    tsusho_phone = models.CharField(max_length=11, blank=True, verbose_name='通所者電話番号')
    tsusho_email = models.EmailField(blank=True, verbose_name='通所者メールアドレス')
    hogo_name = models.CharField(max_length=30, blank=True, verbose_name='保護者氏名')
    hogo_phone = models.CharField(max_length=11, blank=True, verbose_name='保護者電話番号')
    hogo_email = models.EmailField(blank=True, verbose_name='保護者メールアドレス')
    is_active = models.BooleanField(default=True,
        help_text='このユーザーがアクティブかどうかを示します。アカウント削除の代わりにこれを選択解除します。',
        verbose_name='アクティブ'
    )
    tokki_naiyo = models.TextField(max_length=1000, blank=True, verbose_name='特記内容')
    toroku_date = models.DateTimeField(default=timezone.localtime, verbose_name='登録日')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新日')

    def __str__(self):
        return str(self.tsusho_name)
    
    class Meta():
        verbose_name_plural = '通所者情報'

# 消防点検
class Inspection(models.Model):
    torokusha = models.ForeignKey(User, verbose_name='登録者',on_delete=models.PROTECT) 
    syobo_keirokakunin = models.BooleanField(default=False, verbose_name='避難経路確認')
    syobo_syobosetsubi = models.BooleanField(default=False, verbose_name='消防設備')
    syobo_syokakisecchi = models.BooleanField(default=False, verbose_name='消火器設置')
    syobo_kakikakunin = models.BooleanField(default=False, verbose_name='火器確認')
    syobo_suikounetsu = models.BooleanField(default=False, verbose_name='水光熱')
    tokki_naiyo = models.TextField(max_length=1000, blank=True, verbose_name='特記内容')
    toroku_date = models.DateTimeField(default=timezone.localtime, verbose_name='登録日')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新日')

    def __str__(self):
        return str(self.torokusha.username)
    
    class Meta():
        verbose_name_plural = '消防点検情報'

# 日中報告内容
class Dailyreport(models.Model):
    visitor = models.ForeignKey(Visitor, verbose_name='通所者氏名',on_delete=models.PROTECT)
    tanto = models.ForeignKey(User, verbose_name='担当',on_delete=models.PROTECT)
    tokki_naiyo = models.TextField(max_length=1000, blank=True ,verbose_name='特記内容')
    tsusho_unagashi = models.BooleanField(default=False, verbose_name='通所促し')
    taityomen = models.CharField(max_length=15, blank=True, verbose_name='体調面')
    HAISETSU_CHOICES = (
        (0, '未'),
        (1, '小'),
        (2, '中'),
        (3, '大'),
    )
    haisetsu = models.IntegerField(default=0, null=True, blank=True, choices=HAISETSU_CHOICES, verbose_name='排泄')
    kenon_1 = models.CharField(max_length=30, blank=True, verbose_name='検温１')
    kenon_2 = models.CharField(max_length=30, blank=True, verbose_name='検温２')
    chushoku = models.CharField(max_length=30, blank=True, verbose_name='昼食')
    suibun = models.CharField(max_length=30, blank=True, verbose_name='水分')
    sogei_1 = models.CharField(max_length=30, blank=True, verbose_name='送迎 行')
    sogei_2 = models.CharField(max_length=30, blank=True, verbose_name='送迎 帰')
    shozai_jikan_1 = models.TimeField(null=True, blank=True, verbose_name='所在 時間１')
    shozai_jikan_2 = models.TimeField(null=True, blank=True, verbose_name='所在 時間２')
    denwa_shien_1 = models.BooleanField(default=False, verbose_name='電話支援１')
    denwa_shien_2 = models.BooleanField(default=False, verbose_name='電話支援２')
    kesseki = models.BooleanField(default=False, verbose_name='欠席')
    kesseki_kasan = models.BooleanField(default=False, verbose_name='欠席加算')
    toroku_date = models.DateTimeField(default=timezone.localtime, verbose_name='登録日')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新日')

    def __str__(self):
        return str(self.visitor.tsusho_name)
    
    class Meta():
        verbose_name_plural = '日中報告内容'