# Generated by Django 4.2.2 on 2023-06-21 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_reviveuser_groups_reviveuser_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviveuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
