# Generated by Django 2.2.12 on 2020-05-27 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyst',
            name='full_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
