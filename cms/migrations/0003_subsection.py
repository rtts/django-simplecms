import ckeditor.fields
import cms.models
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='position')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('color', models.PositiveIntegerField(choices=[(1, 'Licht'), (2, 'Donker')], default=1, verbose_name='color')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='content')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='image')),
                ('button_text', cms.models.VarCharField(blank=True, verbose_name='button text')),
                ('button_link', cms.models.VarCharField(blank=True, verbose_name='button link')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subsections', to='cms.Section', verbose_name='section')),
            ],
            options={
                'verbose_name': 'subsection',
                'verbose_name_plural': 'subsections',
                'ordering': ['position'],
            },
        ),
    ]
