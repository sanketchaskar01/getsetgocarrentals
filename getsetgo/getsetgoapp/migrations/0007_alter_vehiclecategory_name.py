# Generated by Django 5.1 on 2024-09-12 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getsetgoapp', '0006_remove_vehiclecategory_vehiclecategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclecategory',
            name='name',
            field=models.CharField(default='Unknown Category', max_length=50),
        ),
    ]
