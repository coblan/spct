"""sportscenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from helpers.authuser import urls as authuser_urls
from hello.engine_menu import PcMenu
from django.views.generic import RedirectView 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/',include(authuser_urls)),
    
    url(r'^pc/([\w\.]+)/?$',PcMenu.as_view(),name=PcMenu.url_name),
    url(r'^main/',include('maindb.urls')),
    
    url(r'^d/',include('helpers.director.urls'),name='director'),
    url(r'^$',RedirectView.as_view(url='/pc/maindb.account'))    
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
#from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import AUTO_URL
#AUTO_URL(globals())