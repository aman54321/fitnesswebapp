# Generated by Django 4.2 on 2023-05-11 04:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitnessapp', '0010_userdiet_foodname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailycalorietarget',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
