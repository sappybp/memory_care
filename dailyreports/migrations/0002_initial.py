# Generated by Django 5.0.2 on 2024-11-19 00:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("dailyreports", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="dailyreport",
            name="tanto",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name="担当",
            ),
        ),
        migrations.AddField(
            model_name="inspection",
            name="torokusha",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name="登録者",
            ),
        ),
        migrations.AddField(
            model_name="dailyreport",
            name="visitor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="dailyreports.visitor",
                verbose_name="通所者氏名",
            ),
        ),
    ]
