# Generated by Django 4.1.2 on 2022-11-28 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_transactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='infirmaryorder',
            name='final_receipt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='final_receipt', to='users.medicaldocuments'),
        ),
    ]