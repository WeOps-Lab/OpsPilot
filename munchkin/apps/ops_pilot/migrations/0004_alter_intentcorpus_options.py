# Generated by Django 4.2.7 on 2024-04-29 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ops_pilot', '0003_alter_intent_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='intentcorpus',
            options={'verbose_name': '语料', 'verbose_name_plural': '语料'},
        ),
    ]
