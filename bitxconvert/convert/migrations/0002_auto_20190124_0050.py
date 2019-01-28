# Generated by Django 2.0.10 on 2019-01-24 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversion',
            name='exchange',
            field=models.CharField(choices=[('BINANCE', 'BINANCE'), ('BITTREX', 'BITTREX'), ('COINBASE', 'COINBASE')], max_length=50),
        ),
        migrations.AlterField(
            model_name='conversion',
            name='tax_service',
            field=models.CharField(choices=[('MANUAL', 'MANUAL'), ('CRYPTOTRADER', 'CRYPTOTRADER.TAX'), ('BITCOINTAX', 'BITCOIN.TAX')], max_length=100),
        ),
    ]
