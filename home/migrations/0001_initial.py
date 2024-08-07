# Generated by Django 5.0.4 on 2024-06-06 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('module_id', models.AutoField(primary_key=True, serialize=False)),
                ('module_code', models.SlugField(blank=True, max_length=100, unique=True)),
                ('module_name', models.CharField(max_length=200)),
                ('parent_module', models.ManyToManyField(blank=True, related_name='child_module', to='home.module')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyModule',
            fields=[
                ('cm_id', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.companyprofile')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.module')),
            ],
        ),
    ]
