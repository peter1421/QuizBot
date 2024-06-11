# Generated by Django 2.1.15 on 2024-04-27 07:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_siteuser_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteuser",
            name="email",
            field=models.EmailField(
                blank=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="電子郵件地址",
            ),
        ),
        migrations.AlterField(
            model_name="siteuser",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID",
            ),
        ),
    ]
