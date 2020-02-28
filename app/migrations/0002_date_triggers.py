from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("app", "0001_initial")]

    operations = [
        migrations.RunSQL(
            """
create function set_created_at() returns trigger language plpgsql as
$$
begin
    if TG_OP = 'INSERT' then
        NEW.created_at = now();
    elsif TG_OP = 'UPDATE' then
        NEW.created_at = OLD.created_at;
    end if;

    return NEW;
end;
$$;

create function set_updated_at() returns trigger language plpgsql as
$$
begin
    NEW.updated_at = now();
    return NEW;
end;
$$;

create trigger set_created_at before insert or update on app_user for each row execute procedure set_created_at();
create trigger set_updated_at before insert or update on app_user for each row execute procedure set_updated_at();

create trigger set_created_at before insert or update on app_map for each row execute procedure set_created_at();
create trigger set_updated_at before insert or update on app_map for each row execute procedure set_updated_at();

create trigger set_created_at before insert or update on app_place for each row execute procedure set_created_at();
create trigger set_updated_at before insert or update on app_place for each row execute procedure set_updated_at();

create trigger set_created_at before insert or update on app_evaluation for each row execute procedure set_created_at();
create trigger set_updated_at before insert or update on app_evaluation for each row execute procedure set_updated_at();

create trigger set_created_at before insert or update on app_tag for each row execute procedure set_created_at();
create trigger set_updated_at before insert or update on app_tag for each row execute procedure set_updated_at();
""",
            """
drop trigger set_created_at on app_user;
drop trigger set_updated_at on app_user;
drop trigger set_created_at on app_map;
drop trigger set_updated_at on app_map;
drop trigger set_created_at on app_place;
drop trigger set_updated_at on app_place;
drop trigger set_created_at on app_tag;
drop trigger set_updated_at on app_tag;
drop trigger set_created_at on app_evaluation;
drop trigger set_updated_at on app_evaluation;
drop function set_created_at();
drop function set_updated_at();

                """,
        )
    ]
