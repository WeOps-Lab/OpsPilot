# Generated by Django 4.2.7 on 2024-06-10 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentpack_mgmt', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botactions',
            name='llm_skill',
        ),
        migrations.AlterField(
            model_name='botactions',
            name='name',
            field=models.CharField(max_length=255, verbose_name='动作名称'),
        ),
    ]