# Generated by Django 2.2.28 on 2025-03-26 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ROS_App', '0016_auto_20250326_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
