# Generated by Django 3.0.7 on 2020-07-22 00:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200721_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='beforeemailverification',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
