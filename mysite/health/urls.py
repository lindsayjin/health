from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^input/$', views.input, name = 'input'),
    url(r'^optionalinput/$', views.optionalinput, name = 'optionalinput'),
    url(r'^result/$', views.result, name = 'result')
    #url(r'^optionalinput/(?P<port>[a-z]+)/(?P<year>[0-9]{4})/(?P<em1>[0-9]+)/(?P<em2>[0-9]+)/(?P<em3>[0-9]+)/$', views.input, name = 'input')
    #url(r'^result/(?P<conc>\d*\.*\d*)/(?P<y1>[0-9]{2})/(?P<y2>[0-9]{2})/(?P<y3>[0-9]{2})/(?P<pop>[0-9]+)/$', views.result, name = 'result')
]