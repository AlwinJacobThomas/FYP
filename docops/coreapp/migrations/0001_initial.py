# Generated by Django 4.1.7 on 2023-06-16 21:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('hospital', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('appointment_status', models.CharField(choices=[('cancelled', 'Cancelled'), ('pending', 'Pending'), ('completed', 'Completed')], max_length=255)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='d_appointment', to='hospital.doctor')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='h_appointment', to='user.hospitalprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p_appointment', to='user.patientprofile')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('doctor_review', models.TextField(blank=True, null=True)),
                ('hospital_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('hospital_review', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_review', to='coreapp.appointment')),
            ],
        ),
    ]