# Generated by Django 5.0.4 on 2024-06-12 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry', '0014_inquiry_unmerged_order_quantities'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='metadata',
            field=models.JSONField(blank=True, null=True),
        ),
    ]