# Generated by Django 4.1.7 on 2023-03-12 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='well',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
