# Generated by Django 4.2.2 on 2023-06-18 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api', '0005_alter_reviveuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviveuser',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='reviveuser_set', related_query_name='reviveuser', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='reviveuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='reviveuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='reviveuser_set', related_query_name='reviveuser', to='auth.permission', verbose_name='user permissions'),
        ),
    ]