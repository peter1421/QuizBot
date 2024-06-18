# Generated by Django 4.2.9 on 2024-06-18 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chatbot', '0002_chatmessage_created_at_chatmessage_thread_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PythonChatbot',
            fields=[
                ('chatbot_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='chatbot.chatbot')),
            ],
            options={
                'verbose_name': 'Python的聊天機器人',
                'verbose_name_plural': 'Python的聊天機器人們',
            },
            bases=('chatbot.chatbot',),
        ),
        migrations.CreateModel(
            name='PythonChatMessage',
            fields=[
                ('chatmessage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='chatbot.chatmessage')),
            ],
            options={
                'verbose_name': 'Python的聊天訊息',
                'verbose_name_plural': 'Python的聊天訊息們',
            },
            bases=('chatbot.chatmessage',),
        ),
    ]
