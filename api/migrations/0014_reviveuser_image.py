# Generated by Django 4.2.2 on 2023-06-30 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_reviveuser_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviveuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_images'),
        ),
    ]