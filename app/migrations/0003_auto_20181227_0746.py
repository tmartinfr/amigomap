# Generated by Django 2.1.4 on 2018-12-27 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20181226_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='google_place_id',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='app.Tag'),
        ),
    ]