# Generated by Django 5.0.6 on 2024-09-25 06:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='blog/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'gif', 'jpeg'])]),
        ),
    ]
