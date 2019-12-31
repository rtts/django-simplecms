# Generated by Django 3.0.1 on 2019-12-31 11:16

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='position')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('type', models.CharField(choices=[('normal', 'Normaal')], default='normal', max_length=16, verbose_name='section type')),
                ('color', models.PositiveIntegerField(choices=[(1, 'Wit')], default=1, verbose_name='color')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='content')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='image')),
                ('video', embed_video.fields.EmbedVideoField(blank=True, help_text='Paste a YouTube, Vimeo, or SoundCloud link', verbose_name='video')),
                ('button_text', models.CharField(blank=True, max_length=255, verbose_name='button text')),
                ('button_link', models.CharField(blank=True, max_length=255, verbose_name='button link')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='cms.Page', verbose_name='page')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_app.section_set+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImageSection',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('app.section',),
        ),
        migrations.CreateModel(
            name='TextSection',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('app.section',),
        ),
    ]
