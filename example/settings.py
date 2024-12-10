import os
import random
import string
import sys

PROJECT_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

DEBUG = "runserver" in sys.argv
KEYFILE = f"/tmp/{PROJECT_NAME}.secret"
ADMINS = [("Jaap Joris Vens", "jj@rtts.eu")]
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = PROJECT_NAME + ".urls"
WSGI_APPLICATION = PROJECT_NAME + ".wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "nl"
TIME_ZONE = "Europe/Amsterdam"
STATIC_URL = "/static/"
STATIC_ROOT = "/srv/" + PROJECT_NAME + "/static"
MEDIA_URL = "/media/"
MEDIA_ROOT = "/srv/" + PROJECT_NAME + "/media"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    CACHE_MIDDLEWARE_SECONDS = 0

try:
    with open(KEYFILE) as f:
        SECRET_KEY = f.read()
except IOError:
    SECRET_KEY = "".join(random.choice(string.printable) for x in range(50))
    with open(KEYFILE, "w") as f:
        f.write(SECRET_KEY)

INSTALLED_APPS = [
    PROJECT_NAME,
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cms",
    "embed_video",
    "easy_thumbnails",
]
if not DEBUG:
    INSTALLED_APPS += ["django.contrib.staticfiles"]

MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "cms.middleware.SassMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cms.middleware.FetchFromCacheMiddleware",
    "tidy.middleware.TidyMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": PROJECT_NAME,
        "NAME": PROJECT_NAME,
    }
}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
        "LOCATION": "127.0.0.1:11211",
        "KEY_PREFIX": PROJECT_NAME,
    }
}
