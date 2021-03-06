# Generated by Django 4.0.1 on 2022-02-01 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('softdesk', '0003_remove_project_author_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='author_user_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
