# Generated by Django 2.1.7 on 2019-03-14 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentregister',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='appointmentregister',
            name='time_utilized',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='appointmentregister',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registered_users', to='appointments.Appointment'),
        ),
    ]
