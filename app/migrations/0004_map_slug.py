# Generated by Django 2.1.5 on 2019-01-27 16:37


from django.db import migrations, models
import faker
import slugify


class Migration(migrations.Migration):

    dependencies = [("app", "0003_auto_20181227_0746")]

    operations = [
        migrations.AddField(
            model_name="map", name="slug", field=models.SlugField(unique=True)
        )
    ]
