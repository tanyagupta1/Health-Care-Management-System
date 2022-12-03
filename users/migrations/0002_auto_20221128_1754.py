# Generated by Django 3.2.16 on 2022-11-28 12:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import users.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocRequestHospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_fulfilled', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='medicaldocuments',
            old_name='hospital',
            new_name='verifier',
        ),
        migrations.RemoveField(
            model_name='medicaldocuments',
            name='patient',
        ),
        migrations.AddField(
            model_name='hospital',
            name='description',
            field=models.TextField(default='na', null=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='image_1',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.file_size]),
        ),
        migrations.AddField(
            model_name='hospital',
            name='image_2',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.file_size]),
        ),
        migrations.AddField(
            model_name='infirmary',
            name='description',
            field=models.TextField(default='na', null=True),
        ),
        migrations.AddField(
            model_name='infirmary',
            name='image_1',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.file_size]),
        ),
        migrations.AddField(
            model_name='infirmary',
            name='image_2',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.file_size]),
        ),
        migrations.AddField(
            model_name='infirmary',
            name='wallet',
            field=models.PositiveIntegerField(default=1000000, null=True),
        ),
        migrations.AddField(
            model_name='insurancecompany',
            name='description',
            field=models.TextField(default='na', null=True),
        ),
        migrations.AddField(
            model_name='insurancecompany',
            name='image_1',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.file_size]),
        ),
        migrations.AddField(
            model_name='insurancecompany',
            name='image_2',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.file_size]),
        ),
        migrations.AddField(
            model_name='insurancecompany',
            name='wallet',
            field=models.IntegerField(default=1000000, null=True),
        ),
        migrations.AddField(
            model_name='medicaldocuments',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user_auth'),
        ),
        migrations.AddField(
            model_name='medicaldocuments',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='wallet',
            field=models.PositiveIntegerField(default=1000000, null=True),
        ),
        migrations.AddField(
            model_name='user_auth',
            name='is_authenticated',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='fullname',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.RegexValidator('[!@#$%^&*()_+-=~`[]{}|;\\\'",./<>?]', inverse_match=True)]),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='location',
            field=models.CharField(default='Delhi', max_length=200, null=True, validators=[django.core.validators.RegexValidator('[!@#$%^&*()_+-=~`[]{}|;\\\'",./<>?]', inverse_match=True)]),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user_auth'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='verification_doc',
            field=models.FileField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.validate_file_extension, users.validators.file_size]),
        ),
        migrations.AlterField(
            model_name='infirmary',
            name='fullname',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.RegexValidator('[!@#$%^&*()_+-=~`[]{}|;\\\'",./<>?]', inverse_match=True)]),
        ),
        migrations.AlterField(
            model_name='infirmary',
            name='location',
            field=models.CharField(default='Delhi', max_length=200, null=True, validators=[django.core.validators.RegexValidator('[!@#$%^&*()_+-=~`[]{}|;\\\'",./<>?]', inverse_match=True)]),
        ),
        migrations.AlterField(
            model_name='infirmary',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user_auth'),
        ),
        migrations.AlterField(
            model_name='infirmary',
            name='verification_doc',
            field=models.FileField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.validate_file_extension, users.validators.file_size]),
        ),
        migrations.AlterField(
            model_name='insurancecompany',
            name='fullname',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.RegexValidator('[!@#$%^&*()_+-=~`[]{}|;\\\'",./<>?]', inverse_match=True)]),
        ),
        migrations.AlterField(
            model_name='insurancecompany',
            name='location',
            field=models.CharField(default='Delhi', max_length=200, null=True, validators=[django.core.validators.RegexValidator('[!@#$%^&*()_+-=~`[]{}|;\\\'",./<>?]', inverse_match=True)]),
        ),
        migrations.AlterField(
            model_name='insurancecompany',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user_auth'),
        ),
        migrations.AlterField(
            model_name='insurancecompany',
            name='verification_doc',
            field=models.FileField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.validate_file_extension, users.validators.file_size]),
        ),
        migrations.AlterField(
            model_name='medicaldocuments',
            name='medical_doc',
            field=models.FileField(null=True, upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='fullname',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.RegexValidator('[!@#$%^&*()_+-=~`[]{}|;\\\'",./<>?]', inverse_match=True)]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user_auth'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='verification_doc',
            field=models.FileField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.validate_file_extension, users.validators.file_size]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pics', validators=[users.validators.file_size]),
        ),
        migrations.AlterField(
            model_name='viewaccess',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user_auth'),
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, null=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to='users.user_auth')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='users.user_auth')),
            ],
        ),
        migrations.CreateModel(
            name='RequestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.medicaldocuments')),
                ('request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.docrequesthospital')),
            ],
        ),
        migrations.CreateModel(
            name='InsuranceRefund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refund_amount', models.IntegerField(default=0, null=True)),
                ('doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.medicaldocuments')),
                ('insurance_company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.insurancecompany')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
        ),
        migrations.CreateModel(
            name='InfirmaryOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.IntegerField(default=0, null=True)),
                ('description', models.TextField(default='na', null=True)),
                ('is_fulfilled', models.BooleanField(default=False, null=True)),
                ('doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.medicaldocuments')),
                ('final_receipt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='final_receipt', to='users.medicaldocuments')),
                ('infirmary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.infirmary')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
        ),
        migrations.AddField(
            model_name='docrequesthospital',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.hospital'),
        ),
        migrations.AddField(
            model_name='docrequesthospital',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.patient'),
        ),
    ]
