# Generated by Django 5.0.6 on 2024-06-04 04:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField(blank=True, null=True)),
                ('generated_response', models.TextField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('miles', models.FloatField(default=0.0)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_runs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
