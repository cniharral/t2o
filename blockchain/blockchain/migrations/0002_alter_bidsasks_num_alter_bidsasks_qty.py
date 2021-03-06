# Generated by Django 4.0.3 on 2022-03-27 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidsasks',
            name='num',
            field=models.IntegerField(unique=True, verbose_name='num'),
        ),
        migrations.AlterField(
            model_name='bidsasks',
            name='qty',
            field=models.FloatField(max_length=80, verbose_name='qty'),
        ),
    ]
