# Generated by Django 4.2 on 2023-05-09 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnessapp', '0004_rename_custom_id_waterintake_user_waterintake_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterintake',
            name='date',
            field=models.DateField(default=datetime.date(2023, 5, 9)),
        ),
    ]
