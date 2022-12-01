# Generated by Django 4.1.3 on 2022-11-30 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '0002_alter_account_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_name', models.CharField(max_length=32, null=True)),
                ('creation_date', models.DateTimeField()),
                ('private', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_owner', to='website.account')),
                ('users', models.ManyToManyField(blank=True, related_name='users_chats', to='website.account')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('sent', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('seen', models.BooleanField(default=False)),
                ('destruct_timer', models.IntegerField(null=True)),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='chat.chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to='website.account')),
            ],
        ),
    ]
