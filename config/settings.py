"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^^jwfvo8!&srf818b9^cxwv6pk^vt3c731wv1iiulg84u9qa03'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
]
# django rest framework를 설치한 다음에 INSTALLED_APPS에 추가해줘야 한다고 적혀있음.

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "common.apps.CommonConfig",
    "experiences.apps.ExperiencesConfig",
    "categories.apps.CategoriesConfig",
    "reviews.apps.ReviewsConfig",
    "wishlists.apps.WishlistsConfig",
    "bookings.apps.BookingsConfig",
    "medias.apps.MediasConfig",
    "direct_messages.apps.DirectMessagesConfig",
    # 각 앱의 apps.py의 클래스 이름을 그대로 넣어주면 된다.
    "testAPP.apps.TestappConfig",
]
# python manage.py startapp {앱이름}으로 새로운 앱을 만들면 항상 INSTALLED_APPS에 추가시켜줘야 한다.

SYSTEM_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = CUSTOM_APPS+SYSTEM_APPS+THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth

AUTH_USER_MODEL = "users.User"
# "{앱 이름}.{모델 이름}"

MEDIA_ROOT = "uploads"
# django에서 파일 업로드를 했을때 서버의 어느 폴더에 위치하게 될지 알려주는 코드
MEDIA_URL = "user-uploads/"
# 이건 파일을 사용자에게 노출하는 방법이고, 위에꺼는 서버에 파일이 실제로 있는 위치.
PAGE_SIZE = 3

REST_FRAMEWORK={
    "DEFAULT_AUTHENTICATION_CLASSES":[
        "rest_framework.authentication.SessionAuthentication",
        "config.authentication.TrustMeBroAuthentication",
    ]
    # 위에서부터 순서대로 user를 찾는다.
}