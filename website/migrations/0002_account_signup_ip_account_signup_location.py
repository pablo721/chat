# Generated by Django 4.1.3 on 2023-02-08 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='signup_ip',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='signup_location',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
