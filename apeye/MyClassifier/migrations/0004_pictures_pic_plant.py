# Generated by Django 2.1.7 on 2019-03-29 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyClassifier', '0003_auto_20190330_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='pictures',
            name='pic_plant',
            field=models.TextField(max_length=100, null=True),
        ),
    ]
