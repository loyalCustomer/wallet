# Generated by Django 3.1.7 on 2021-04-01 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swallet', '0002_auto_20210331_2121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='username',
            new_name='user_id',
        ),
        migrations.AlterField(
            model_name='simplewallet',
            name='wallet_name',
            field=models.CharField(max_length=250, verbose_name='произвольное имя'),
        ),
    ]
