# Generated by Django 2.2 on 2019-05-02 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyClassifier', '0011_auto_20190502_0216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plant',
            old_name='PLANT_name',
            new_name='descrption',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='PLANT_state',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='PLANT_pic',
            new_name='pic',
        ),
        migrations.AddField(
            model_name='plant',
            name='state',
            field=models.TextField(null=True),
        ),
    ]