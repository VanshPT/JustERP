# Generated by Django 5.0.4 on 2024-06-07 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry', '0007_remove_inquiry_credit_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='truckdetails',
            name='truck_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inquiry.trucktype'),
        ),
    ]