import os, string, random

try:
    import uwsgi
    SECRET_KEY = ''.join(random.choice(string.printable) for x in range(50))
    DEBUG = False
except ImportError:
    SECRET_KEY = 'abc'
    DEBUG = True

PROJECT_NAME = INSERT_PROJECT_NAME_HERE
ADMINS = [('JJ Vens', 'jj@rtts.eu')]
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = '/srv/' + PROJECT_NAME + '/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/srv/' + PROJECT_NAME + '/media'
LOGIN_REDIRECT_URL = '/'

SECTION_TYPES = [
    ('normal', 'Normaal'),
]

SECTION_COLORS = [
    (1, 'Wit'),
]

CKEDITOR_CONFIGS = {
    'default': {
        'removePlugins': 'elementspath',
        'extraPlugins': 'format',
        'width': '100%',
        'toolbar': 'Custom',
        # 'contentsCss': STATIC_URL + 'ckeditor.css',
        # 'allowedContent': True, # this allows iframes, embeds, scripts, etc...
        'toolbar_Custom': [
            ['Format'],
            ['Bold', 'Italic', 'Underline', 'TextColor'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
        ],
    }
}

INSTALLED_APPS = [
    'simplesass',
    PROJECT_NAME,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cms',
    'ckeditor',
    'embed_video',
    'easy_thumbnails',
    'django_extensions',
]

MIDDLEWARE = [
    'simplesass.middleware.SimpleSassMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': PROJECT_NAME,
        'NAME': PROJECT_NAME,
    }
}
