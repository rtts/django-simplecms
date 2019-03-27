Django Simple CMS
=================

Simple CMS app with models that should suit everyone's small website needs.

Installation
------------

    pip install git+https://github.com/rtts/django-simplecms.git

Configuration
-------------

Add the following to your Django settings:

    INSTALLED_APPS += [
        'cms',
        'ckeditor',
        'embed_video',
        'easy_thumbnails',
    ]

    SECTION_TYPES = [
        ('normal', 'Normaal'),
    ]

    SECTION_COLORS = [
        (1, 'Licht'),
        (2, 'Donker'),
    ]

And add the following to your URL patterns:

    urlpatterns += [
        path('accounts/', include('django.contrib.auth.urls')),
        path('', include('cms.urls', namespace='cms')),
    ]
