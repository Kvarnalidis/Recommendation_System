# Generated by Django 2.1.5 on 2019-09-06 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shights', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sights',
            name='Image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
