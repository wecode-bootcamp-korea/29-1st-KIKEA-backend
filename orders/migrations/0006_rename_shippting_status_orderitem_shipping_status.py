# Generated by Django 3.2.10 on 2022-02-02 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderitem_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='shippting_status',
            new_name='shipping_status',
        ),
    ]
