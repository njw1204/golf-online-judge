# Generated by Django 2.1.8 on 2019-05-03 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_auto_20190502_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solvepost',
            name='lang',
            field=models.PositiveSmallIntegerField(choices=[(1, 'python3')], default=1),
        ),
    ]
