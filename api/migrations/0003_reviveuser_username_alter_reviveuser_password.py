# Generated by Django 4.2.2 on 2023-06-14 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_user_reviveuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviveuser',
            name='username',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reviveuser',
            name='password',
            field=models.CharField(max_length=250),
        ),
    ]