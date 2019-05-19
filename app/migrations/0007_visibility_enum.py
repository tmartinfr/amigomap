from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("app", "0006_remove_place_color")]

    operations = [
        migrations.RunSQL(
            """
            create type visibility as enum ('public', 'private');
            alter table app_map alter column visibility
                                type visibility using visibility::visibility;
            """,
            """
            alter table app_map
                alter column visibility type character varying(32);
            drop type visibility;
            """,
        )
    ]
