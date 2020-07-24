# Generated by Django 3.0.7 on 2020-07-23 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200722_0338'),
    ]

    operations = [
        migrations.CreateModel(
            name='boxes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box_num', models.IntegerField()),
                ('available', models.BooleanField()),
                ('associeted_customer', models.EmailField(max_length=254)),
                ('filledTime', models.DateTimeField()),
            ],
        ),
    ]
