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
from hello.engine_menu import PcMenu, ProgramerAdmin,YunweiEngin
from django.views.generic import RedirectView 
from maindb.views import test
from helpers.authuser.engin_view import AuthEngine
from maindb.views import Notice, Help,Activity,TestAppH5View #,ActivityIndex
from helpers.director.views import director_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^accounts/',include(authuser_urls)),
    url(r'^accounts/([\w\.]+)/?$',AuthEngine.as_view(),name=AuthEngine.url_name),
    url(r'^notice/(?P<name>[^/]+)/?$', Notice.as_view()), 
    url(r'^help/(?P<name>[^/]+)/?$', Help.as_view()),
    
    #url(r'^actv2/index?$', ActivityIndex.as_view()),
    url(r'^actv2/(?P<pk>[^/]+)/?$', Activity.as_view()),
    url(r'^app_h5/?$', TestAppH5View.as_view()),
     
    url(r'^pc/([\w\.]+)/?$',PcMenu.as_view(),name=PcMenu.url_name),
    url(r'^main/',include('maindb.urls')),
    
    url(r'^d/',include('helpers.director.urls'),name='director'),
    url(r'^dapi/(?P<director_name>[\w\/\.]+)?/?$',director_view),
    
    url(r'^pa/([\w\.]+)/?$', ProgramerAdmin.as_view(), name= ProgramerAdmin.url_name), 
    url(r'^pa/?$', RedirectView.as_view(url='/pa/marketgroup')), 
    
    url(r'^yw/([\w\.]+)/?$', YunweiEngin.as_view(), name= YunweiEngin.url_name), 
    url(r'^yw/?$', RedirectView.as_view(url='/yw/domain')), 
    
    
    url(r'^$',RedirectView.as_view(url='/pc/home')) ,
    #url(r'test',test)
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import AUTO_URL
AUTO_URL(globals())