# Generated by Django 5.0.4 on 2024-06-09 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry', '0013_alter_creditdays_credit_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='unmerged_order_quantities',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]