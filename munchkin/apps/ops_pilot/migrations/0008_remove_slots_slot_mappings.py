# Generated by Django 4.2.7 on 2024-04-29 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ops_pilot', '0007_slots'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slots',
            name='slot_mappings',
        ),
    ]
