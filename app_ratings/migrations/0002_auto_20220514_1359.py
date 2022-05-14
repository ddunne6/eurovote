# Generated by Django 3.2.3 on 2022-05-14 12:59

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_ratings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='name',
        ),
        migrations.AddField(
            model_name='country',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]