# Generated by Django 4.1.7 on 2024-02-14 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_file_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='folder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folders_within', to='mainapp.folder'),
        ),
    ]
