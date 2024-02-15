# Generated by Django 4.1.7 on 2024-02-15 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_folder_folder'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='folder',
            constraint=models.UniqueConstraint(fields=('folder', 'name'), name='unique_folder_name'),
        ),
    ]
