# Generated by Django 5.0.4 on 2024-05-01 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0002_alter_serving_addedsugars_alter_serving_protein_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serving',
            old_name='food',
            new_name='name',
        ),
    ]
