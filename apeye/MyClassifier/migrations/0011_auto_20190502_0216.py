# Generated by Django 2.2 on 2019-05-02 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyClassifier', '0010_auto_20190501_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='PRODUCT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(null=True)),
                ('name', models.TextField(null=True)),
                ('price', models.IntegerField(null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_biological_control',
            new_name='biological_control',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_chemical_control',
            new_name='chemicalcontrol',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_nutshell',
            new_name='nutshell',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_pic',
            new_name='pic',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_plants',
            new_name='plants',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_preventive_mesures',
            new_name='preventivemesures',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_scientific_name',
            new_name='scientific_name',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_symptoms',
            new_name='symptoms',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='disease_trigger',
            new_name='trigger',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='mobile_number',
            new_name='mobilenumber',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_name',
            new_name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='disease',
            name='diseasetype',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='DiseasePlant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Disease', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MyClassifier.Disease')),
                ('PLANT', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MyClassifier.PLANT')),
            ],
        ),
        migrations.AddField(
            model_name='disease',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MyClassifier.PRODUCT'),
        ),
    ]
