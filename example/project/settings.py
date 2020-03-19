import os, random, string
try:
    import uwsgi
    DEBUG = False
except ImportError:
    DEBUG = True
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PROJECT_NAME = 'example'
KEYFILE = f'/tmp/{PROJECT_NAME}.secret'
ADMINS = [('JJ Vens', 'jj@rtts.eu')]
DEFAULT_TO_EMAIL = 'jj@rtts.eu'
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
CMS_SECTION_MODEL = 'app.Section'
CMS_PAGE_MODEL = 'app.Page' # https://github.com/wq/django-swappable-models/issues/18#issuecomment-514039164
MARKDOWN_EXTENSIONS = ['extra', 'smarty']

def read(file):
    with open(file) as f:
        return f.read()
def write(file, content):
    with open(file, 'w') as f:
        f.write(content)
try:
    SECRET_KEY = read(KEYFILE)
except IOError:
    SECRET_KEY = ''.join(random.choice(string.printable) for x in range(50))
    write(KEYFILE, SECRET_KEY)

INSTALLED_APPS = [
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cms',
    'polymorphic',
    'embed_video',
    'easy_thumbnails',
    'django_extensions',
]

MIDDLEWARE = [
    'cms.middleware.SassMiddleware',
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
