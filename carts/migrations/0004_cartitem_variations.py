# Generated by Django 5.1.7 on 2025-03-19 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_taxsetting'),
        ('store', '0003_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
