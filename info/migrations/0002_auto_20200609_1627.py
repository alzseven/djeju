# Generated by Django 3.0.6 on 2020-06-09 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sido',
            name='qur_rate',
            field=models.CharField(max_length=30),
        ),
    ]