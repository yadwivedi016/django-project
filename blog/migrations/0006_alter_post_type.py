# Generated by Django 5.0.6 on 2024-09-27 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[(1, 'Others'), (2, 'Java'), (3, 'C++'), (4, 'Javascripts'), (5, 'MySQL'), (6, 'Python')], max_length=6),
        ),
    ]
