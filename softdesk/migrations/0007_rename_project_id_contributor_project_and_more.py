# Generated by Django 4.0.1 on 2022-02-03 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('softdesk', '0006_alter_contributor_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contributor',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='contributor',
            old_name='user_id',
            new_name='user',
        ),
    ]
