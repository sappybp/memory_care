# Generated by Django 5.0.2 on 2024-10-19 16:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dailyreports", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailyreport",
            name="toroku_date",
            field=models.DateTimeField(
                default=django.utils.timezone.localtime, verbose_name="登録日"
            ),
        ),
        migrations.AlterField(
            model_name="inspection",
            name="toroku_date",
            field=models.DateTimeField(
                default=django.utils.timezone.localtime, verbose_name="登録日"
            ),
        ),
        migrations.AlterField(
            model_name="visitor",
            name="toroku_date",
            field=models.DateTimeField(
                default=django.utils.timezone.localtime, verbose_name="登録日"
            ),
        ),
    ]
