# Generated by Django 5.1.7 on 2025-03-12 12:00

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=100, populate_from='name', unique=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='photos/category')),
            ],
        ),
    ]
