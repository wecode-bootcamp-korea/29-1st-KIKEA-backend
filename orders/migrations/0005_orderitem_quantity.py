# Generated by Django 3.2.10 on 2022-02-02 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_orderitem_tracking_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
