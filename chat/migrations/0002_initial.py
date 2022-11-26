# Generated by Django 4.0.5 on 2022-07-06 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spybot', '0001_initial'),
        ('chat', '0001_initial'),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_creator', to='website.profile'),
        ),
        migrations.AddField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='room_users', to='website.profile'),
        ),
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message_chat', to='chat.chat'),
        ),
        migrations.AddField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message_recipient', to='website.profile'),
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message_room', to='chat.room'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to='website.profile'),
        ),
        migrations.AddField(
            model_name='message',
            name='watchlists',
            field=models.ManyToManyField(related_name='message_watchlists', to='spybot.watchlist'),
        ),
        migrations.AddField(
            model_name='chat',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_creator', to='website.profile'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_recipient', to='website.profile'),
        ),
    ]
