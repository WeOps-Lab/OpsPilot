# Generated by Django 4.2.7 on 2024-06-05 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_mgmt', '0003_bot_bot_domain_bot_enable_bot_domain_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='enable_ssl',
            field=models.BooleanField(default=False, verbose_name='启用SSL'),
        ),
    ]
