# Generated by Django 3.0.2 on 2020-02-16 14:27

import cms.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True, verbose_name='number')),
                ('title', cms.models.VarCharField(verbose_name='title')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='slug')),
                ('menu', models.BooleanField(default=True, verbose_name='visible in menu')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'ordering': ['number'],
                'abstract': False,
            },
            bases=(cms.models.Numbered, models.Model),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', cms.models.VarCharField(blank=True, verbose_name='type')),
                ('number', models.PositiveIntegerField(blank=True, verbose_name='number')),
                ('title', cms.models.VarCharField(blank=True, verbose_name='title')),
                ('content', models.TextField(blank=True, verbose_name='content')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='image')),
                ('video', embed_video.fields.EmbedVideoField(blank=True, help_text='Paste a YouTube, Vimeo, or SoundCloud link', verbose_name='video')),
                ('href', cms.models.VarCharField(blank=True, verbose_name='button link')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sections', to=settings.CMS_PAGE_MODEL, verbose_name='page')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_app.section_set+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
                'ordering': ['number'],
                'abstract': False,
            },
            bases=(cms.models.Numbered, models.Model),
        ),
    ]
