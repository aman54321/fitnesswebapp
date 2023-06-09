# Generated by Django 4.2 on 2023-05-11 05:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fitnessapp', '0012_alter_dailycalorietarget_date_added'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='A_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='activity',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activity',
            name='calories_burned',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='activity',
            name='steps',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='activity',
            name='workout_duration',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together={('user', 'date')},
        ),
    ]
