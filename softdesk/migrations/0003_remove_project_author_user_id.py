# Generated by Django 4.0.1 on 2022-02-01 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('softdesk', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='author_user_id',
        ),
    ]