# Generated by Django 5.0.4 on 2024-06-02 08:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='modules',
            field=models.ManyToManyField(to='home.module'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='permissions',
            field=models.ManyToManyField(to='authapp.permission'),
        ),
        migrations.AddField(
            model_name='profile',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.department'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authapp.profile'),
        ),
    ]
