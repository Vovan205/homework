from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.items, name='itempage'),
    url(r'^test/', views.test, name='mainpage'),
    url(r'^register/$', views.RegistrationFormView.as_view(), name="register"),
    url(r'^login/$', views.LoginFormView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^addtocomment/(?P<pk>\d+)/$', views.addtocomment, name='addtocomment'),
    url(r'^page/(\d+)/$', views.post_list, name='pages'),
    url(r'^edit/$', views.add)
]
