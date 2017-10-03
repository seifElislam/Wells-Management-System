from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^home/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/new/$', views.new_user, name='new_user'),
    url(r'^users/(?P<user_id>[0-9]+)$', views.get_user, name='get_user'),
    url(r'^wells/(?P<well_id>[0-9]+)$', views.well_info, name='well_info'),
    url(r'^fields/$', views.fields, name='fields'),
    url(r'^field/wells/$', views.select_wells, name='select'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^wells/$', views.wells, name='wells'),
    url(r'^operation/$', views.operations, name='operations'),
    url(r'^operation/(?P<well_id>[0-9]+)$', views.well_operations, name='well_operations'),
    url(r'^operation/(?P<well_id>[0-9]+)/new/$', views.add_operations, name='add_operations'),
    url(r'^keys/$', views.add_keys, name='add_keys'),
    url(r'^well/(?P<well_id>[0-9]+)/sketch/(?P<operation_id>[0-9]+)$', views.show_sketch, name='show_sketch'),
    url(r'^schedule/(?P<well_id>[0-9]+)$', views.show_schedule, name='show_schedule'),
    url(r'^wc/$', views.add_wc, name='add_wc')

]