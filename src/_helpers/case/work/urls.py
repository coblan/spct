from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^workindex/?$',views.dir_man,name='work.workindex'),
    # url(r'^model/(?P<name>.*)/$', views.model_view),
]