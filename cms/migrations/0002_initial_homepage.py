from django.db import migrations

def add_homepage(apps, schema_editor):
    Page = apps.get_model('cms', 'Page')
    if not Page.objects.exists():
        Page(slug='', title='Homepage', position=1).save()

class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_homepage, migrations.RunPython.noop),
    ]
