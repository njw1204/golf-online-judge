# Generated by Django 2.1.8 on 2019-04-28 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problempost',
            name='body',
            field=models.TextField(blank=True, max_length=100000),
        ),
        migrations.AlterField(
            model_name='problempost',
            name='example_in',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='problempost',
            name='example_out',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]