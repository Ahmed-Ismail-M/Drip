# Generated by Django 4.0.1 on 2022-02-07 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drip', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jogging',
            name='end',
        ),
    ]