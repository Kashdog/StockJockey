# Generated by Django 2.0.3 on 2018-05-09 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FormExample', '0002_auto_20180509_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeadToHeadMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='firstuser', to='FormExample.Request')),
                ('user2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seconduser', to='FormExample.Request')),
            ],
            options={
                'db_table': 'Headtoheadmatch',
            },
        ),
    ]
