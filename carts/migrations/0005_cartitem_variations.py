# Generated by Django 3.0.3 on 2020-02-24 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_variationmanager'),
        ('carts', '0004_cartitem_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, null=True, to='products.Variation'),
        ),
    ]
