"""DatasetAnnotatorProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from DatasetAnnotator import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'submit/$', views.submit),
    url(r'^(?P<annotator_name>\w{0,10})/$', views.entry_point),
    url(r'^(?P<annotator_name>\w{0,10})/shared$', views.shared_list),
    url(r'^(?P<annotator_name>\w{0,10})/(?P<db_name>\w{0,10})/(?P<question_id>\d{0,20})/$', views.annotation),
]
