# encoding:utf-8
from __future__ import unicode_literals

# 自定义模板，优先级最高
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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


#地区信息
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE='Asia/Shanghai'

# 优先使用app目录下的templates，这样更加便于开发
STATICFILES_FINDERS=[
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
]

# 区别collectstatic命令，赋予不同的static路径
import sys
if 'collectstatic' not in sys.argv:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static').replace('\\', '/'),
    )
else:
    STATIC_ROOT= os.path.join(BASE_DIR, 'static').replace('\\', '/')

#
MEDIA_ROOT= os.path.join( os.path.dirname(BASE_DIR),'media')
MEDIA_URL = '/media/'