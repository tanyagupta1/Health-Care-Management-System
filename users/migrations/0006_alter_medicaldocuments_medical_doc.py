# Generated by Django 4.1.2 on 2022-11-28 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_infirmaryorder_final_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicaldocuments',
            name='medical_doc',
            field=models.FileField(null=True, upload_to='profile_pics'),
        ),
    ]