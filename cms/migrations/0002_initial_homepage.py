import swapper
from django.db import migrations
Page = swapper.load_model('cms', 'Page')

def add_homepage(apps, schema_editor):
    if not Page.objects.exists():
        Page(slug='', title='Homepage', position=1).save()

class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_homepage, migrations.RunPython.noop),
    ]
