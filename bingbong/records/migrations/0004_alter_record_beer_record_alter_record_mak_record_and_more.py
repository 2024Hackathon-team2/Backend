# Generated by Django 5.0.7 on 2024-07-26 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_remove_record_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='beer_record',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='record',
            name='mak_record',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='record',
            name='soju_record',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='record',
            name='wine_record',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
    ]
