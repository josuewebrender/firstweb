# Generated by Django 4.2.4 on 2024-01-25 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vistaTablas', '0003_datasalud_fh_escrituranube_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datasalud',
            old_name='id_maquina',
            new_name='Cargadora',
        ),
        migrations.AddField(
            model_name='datasalud',
            name='id_dispositivo',
            field=models.CharField(default=-89, max_length=50),
            preserve_default=False,
        ),
    ]
