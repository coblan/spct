from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^department$',views.manage_department,name='organize.department'),
    url(r'^_tree_depart/?$',views.tree_department,name='organize.tree_depart'),
    # url(r'^model/(?P<name>.*)/$', views.model_view),
]