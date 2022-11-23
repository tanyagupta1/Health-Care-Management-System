# Generated by Django 4.1.2 on 2022-10-29 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_viewaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='wallet',
            field=models.IntegerField(default=1000000, null=True),
        ),
        migrations.CreateModel(
            name='InfirmaryOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.IntegerField(default=0, null=True)),
                ('description', models.TextField(default='na', null=True)),
                ('doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.medicaldocuments')),
                ('infirmary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.infirmary')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
        ),
    ]
