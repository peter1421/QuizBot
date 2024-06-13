# Generated by Django 4.2.9 on 2024-06-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='phone',
            field=models.CharField(max_length=255, unique=True, verbose_name='手機'),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='username',
            field=models.CharField(blank=True, max_length=254, null=True, unique=True, verbose_name='使用者名稱'),
        ),
    ]
