from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^home/$', views.home , name= 'home'),
    url(r'^login/$', views.loginform , name= 'login'),
    url(r'^logout/$', views.logoutt , name= 'logout'),
    url(r'^register/$', views.userregistrationform, name='register'),
    url(r'^changepassword/$', views.changepassword, name='changepassword'),


]