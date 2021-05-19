# Generated by Django 3.2 on 2021-05-05 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('major', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warcraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('military_area', models.CharField(max_length=200)),
                ('major', models.CharField(max_length=200)),
                ('start_pose', models.CharField(max_length=200)),
                ('end_pose', models.CharField(max_length=200)),
                ('dossier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='war_crfts', to='major.dossier')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('school_name', models.CharField(max_length=200)),
                ('major', models.CharField(max_length=200)),
                ('dossier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schools', to='major.dossier')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200)),
                ('year', models.DateField()),
                ('number', models.PositiveIntegerField()),
                ('color', models.CharField(choices=[('yellow', 'yellow'), ('black', 'black'), ('red', 'red'), ('blue', 'blue')], max_length=50)),
                ('type', models.CharField(max_length=200)),
                ('dossier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='major.dossier')),
            ],
        ),
    ]