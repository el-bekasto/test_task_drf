# Generated by Django 4.2.5 on 2023-09-28 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tg_test', '0002_tguser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tguser',
            old_name='user_id',
            new_name='user',
        ),
    ]