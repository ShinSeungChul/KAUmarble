"""Blue_Marble URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from bluemarble_app import views

urlpatterns = [
    url(r'^$', views.home), #시작 페이지
    url(r'^ing/$', views.index_ing), #DB에 데이터 넘기는 쪽
    url(r'^main/(?P<myname>\d+)/$', views.main), #방 선택하는 페이지
    url(r'^make/(?P<myname>\d+)/$', views.make), #방이름 이름
    url(r'^room/(?P<room_id>\d+)/(?P<myname>\d+)/out/$',views.out),#나가기
    url(r'^room/(?P<room_id>\d+)/room_to_marble/(?P<myname>\d+)/$', views.room_to_marble),#시작버튼 받음
    #url(r'^room/(?P<room_id>\d+)/marble/(?P<myname>\d+)/$', views.marble),#게임 시작
    url(r'^make/ing/(?P<myname>\d+)/$', views.make_ing),
    url(r'^room/(?P<room_id>\d+)/(?P<myname>\d+)/$', views.room), #게임하는 방
    url(r'^game/(?P<name1>[-\w]+)/(?P<name2>[-\w]+)/$', views.game),
    url(r'^game/(?P<name1>[-\w]+)/(?P<name2>[-\w]+)/game/ing/$', views.start_turn),
    url(r'^game/(?P<name1>[-\w]+)/(?P<name2>[-\w]+)/answer/$', views.answer),
    ##
    path('admin/',admin.site.urls),
]
