# Generated by Django 5.1 on 2024-09-12 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getsetgoapp', '0005_booking_is_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiclecategory',
            name='vehiclecategory',
        ),
        migrations.AddField(
            model_name='vehiclecategory',
            name='name',
            field=models.CharField(default='Unknown Category', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='vehiclecategory',
            table='vehicle_category',
        ),
    ]
