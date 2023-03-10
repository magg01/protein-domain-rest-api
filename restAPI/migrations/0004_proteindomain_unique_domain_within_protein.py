# Generated by Django 3.2.4 on 2021-06-28 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restAPI', '0003_alter_protein_protein_id'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='proteindomain',
            constraint=models.UniqueConstraint(fields=('protein_id', 'domain_id', 'start', 'stop'), name='unique_domain_within_protein'),
        ),
    ]
