from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^add_favs/(?P<quote_id>\d+)$', views.add_favs),
    url(r'^remove_fav/(?P<quote_id>\d+)$', views.remove_fav),
    url(r'^all_quotes$', views.add_quote),
    url(r'^user/(?P<user_id>\d+)$', views.user),
]