# Generated by Django 4.2.2 on 2023-06-22 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_reviveuser_is_active_alter_reviveuser_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviveuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reviveuser',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]
