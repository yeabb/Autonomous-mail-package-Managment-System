# Generated by Django 3.0.7 on 2020-07-21 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200719_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('box_num', models.IntegerField()),
                ('entered_date', models.DateTimeField()),
                ('access_code', models.IntegerField()),
            ],
        ),
    ]
