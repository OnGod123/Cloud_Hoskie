# Generated by Django 5.1.4 on 2025-01-05 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_person_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User_login',
        ),
        migrations.AlterField(
            model_name='person',
            name='username',
            field=models.CharField(default='default_username', max_length=255, unique=True),
        ),
    ]
