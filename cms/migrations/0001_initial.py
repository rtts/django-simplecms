import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.PositiveIntegerField(choices=[(10, 'Footer')], unique=True)),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='Inhoud')),
            ],
            options={
                'verbose_name': 'configuration parameter',
                'verbose_name_plural': 'configuration parameters',
                'ordering': ['parameter'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='position')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(blank=True, help_text='A short identifier to use in URLs', unique=True, verbose_name='slug')),
                ('menu', models.BooleanField(default=True, verbose_name='visible in menu')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='position')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('type', models.CharField(choices=[('normal', 'Normaal')], default='normal', max_length=16, verbose_name='section type')),
                ('color', models.PositiveIntegerField(choices=[(1, 'Licht'), (2, 'Donker')], default=1, verbose_name='color')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='content')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='image')),
                ('video', embed_video.fields.EmbedVideoField(blank=True, help_text='Paste a YouTube, Vimeo, or SoundCloud link', verbose_name='video')),
                ('button_text', models.CharField(blank=True, max_length=255, verbose_name='button text')),
                ('button_link', models.CharField(blank=True, max_length=255, verbose_name='button link')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='cms.Page', verbose_name='page')),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
                'ordering': ['position'],
            },
        ),
    ]
