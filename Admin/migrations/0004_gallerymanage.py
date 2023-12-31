# Generated by Django 4.2.3 on 2023-07-17 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0003_eventmanage'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryManage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_images')),
                ('Date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
