# Generated by Django 5.1.2 on 2025-02-26 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancyapp', '0004_alter_userstatus_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatus',
            name='user_created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
