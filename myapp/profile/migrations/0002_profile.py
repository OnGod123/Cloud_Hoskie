# Generated by Django 5.1.1 on 2024-11-04 13:52

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_user_login'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('user_video', models.URLField(blank=True)),
                ('social_media_url', models.URLField(blank=True)),
                ('bio', models.TextField(blank=True)),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_pictures/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.person')),
            ],
        ),
    ]
