# Generated by Django 2.0.5 on 2018-05-25 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='door',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
