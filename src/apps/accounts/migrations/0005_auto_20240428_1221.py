# Generated by Django 2.1.15 on 2024-04-28 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20240427_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='tml_house_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='email',
            field=models.EmailField(max_length=255, null=True, unique=True, verbose_name='電子郵件地址'),
        ),
    ]
