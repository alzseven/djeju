# Generated by Django 3.0.6 on 2020-06-15 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_auto_20200616_0331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitals',
            name='spclAdmTyCd',
        ),
        migrations.AddField(
            model_name='hospitals',
            name='hospTyTpCd',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
