from django.db import migrations

from ..models import Map


class Migration(migrations.Migration):

    dependencies = [("app", "0002_date_triggers")]

    operations = [
        migrations.RunSQL(
            """
            create type visibility as enum({});
            alter table app_map alter column visibility type visibility using visibility::visibility;
            """.format(', '.join([f"'{v.name}'" for v in Map.Visibility]))
        )
    ]
