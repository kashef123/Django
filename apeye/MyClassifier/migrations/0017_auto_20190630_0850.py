# Generated by Django 2.2 on 2019-06-30 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyClassifier', '0016_auto_20190613_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disease',
            name='product',
        ),
        migrations.AddField(
            model_name='disease',
            name='language',
            field=models.TextField(null=True),
        ),
    ]
