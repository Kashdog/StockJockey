# Generated by Django 2.0.3 on 2018-05-11 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FormExample', '0004_remove_stockentry_pps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='pps',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='shares',
        ),
    ]