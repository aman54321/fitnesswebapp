# Generated by Django 4.2 on 2023-05-09 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnessapp', '0009_alter_dailycalorietarget_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdiet',
            name='FoodName',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
