# Generated by Django 4.2.7 on 2024-04-29 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='机器人名称')),
                ('description', models.TextField(verbose_name='机器人描述')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否启用')),
                ('session_expiration_time', models.IntegerField(default=60, verbose_name='会话过期时间')),
                ('carry_over_slots_to_new_session', models.BooleanField(default=True, verbose_name='是否携带槽位到新会话')),
            ],
            options={
                'verbose_name': '机器人',
                'verbose_name_plural': '机器人',
            },
        ),
    ]
