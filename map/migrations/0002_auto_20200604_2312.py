# Generated by Django 3.0.6 on 2020-06-04 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitals',
            name='id',
        ),
        migrations.AlterField(
            model_name='hospitals',
            name='telno',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
