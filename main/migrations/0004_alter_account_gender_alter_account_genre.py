# Generated by Django 4.1 on 2023-05-15 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_searchhistory_usersmusic_musiclist_albumimageurl_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='genre',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
