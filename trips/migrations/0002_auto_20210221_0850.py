# Generated by Django 3.1.7 on 2021-02-21 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trip',
            unique_together=set(),
        ),
    ]