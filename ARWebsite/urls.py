"""ARWebsite URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from MyApp.views import *

urlpatterns = (
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'index.html$', index, name='index'),
    url(r'register.html$', do_register, name='do_register'),
    url(r'login.html$', do_login, name='do_login'),
    url(r'add-model.html$', add_model, name='add_mode'),
    url(r'models.html$', models, name='model'),
    url(r'my-account.html$', my_account, name='my_account'),
    url(r'edit-profile.html$', edit_profile, name='edit_profile'),
    url(r'help.html$', help_page, name='help_page'),
    url(r'view-model.html$', view_model, name='view_model'),
)
