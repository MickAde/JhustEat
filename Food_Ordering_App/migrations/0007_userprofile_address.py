# Generated by Django 5.1.2 on 2024-11-07 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food_Ordering_App', '0006_userprofile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=215, null=True),
        ),
    ]
