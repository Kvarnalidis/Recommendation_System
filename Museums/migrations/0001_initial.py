# Generated by Django 2.1.5 on 2019-09-04 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Museums',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=120)),
                ('Image', models.TextField(default='Image')),
                ('Location', models.TextField(blank=True, default=False)),
                ('description', models.TextField(blank=True, default=False)),
                ('price', models.IntegerField()),
                ('theme', models.CharField(max_length=50)),
                ('discountAvailability', models.BooleanField(default=False)),
                ('pointX', models.IntegerField(default=0)),
                ('pointY', models.IntegerField(default=0)),
            ],
        ),
    ]
