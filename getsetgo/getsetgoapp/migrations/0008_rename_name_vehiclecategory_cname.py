# Generated by Django 5.1 on 2024-09-12 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('getsetgoapp', '0007_alter_vehiclecategory_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiclecategory',
            old_name='name',
            new_name='cname',
        ),
    ]
