# Generated by Django 5.0.4 on 2024-06-07 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry', '0010_alter_truckdetails_truck_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transporter',
            fields=[
                ('tr_id', models.AutoField(primary_key=True, serialize=False)),
                ('truck_details', models.ManyToManyField(to='inquiry.truckdetails')),
            ],
        ),
    ]
