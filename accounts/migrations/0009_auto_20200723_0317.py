# Generated by Django 3.0.7 on 2020-07-23 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_boxes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='boxes',
            new_name='BoxList',
        ),
    ]