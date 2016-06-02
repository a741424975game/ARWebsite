# -*- coding: utf-8 -*-

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
from django.conf.urls.static import static
from django.contrib import admin
from MyApp.views import *

urlpatterns = [
    url(r"^admin/", admin.site.urls),  # admin 管理界面
    url(r'^$', index, name='index'),  # 首页
    url(r'^index.html$', index, name='index'),  # 首页
    url(r'^register.html$', do_register, name='register'),  # 注册页面
    url(r'^login.html$', do_login, name='login'),  # 登陆页面
    url(r'^logout.html$', do_logout, name='logout'),    # 注销
    url(r'^add-model.html$', add_model, name='add_mode'),  # 增加AR模型页面
    url(r'^delete.html$', delete_model, name='delete_mode'),   # 删除模型
    url(r'^models.html$', models, name='model'),  # AR模型列表页面
    url(r'^my-account.html$', my_account, name='my_account'),  # 账户信息页面
    url(r'^edit-profile.html$', edit_profile, name='edit_profile'),  # 账户管理页面
    url(r'^help.html$', help_page, name='help_page'),  # 帮助页面
    url(r'^view-model.html$', view_model, name='view_model'),  # 查看AR模型详细信息页面
    url(r'^arConfigInfo-api$', ar_config_info_api, name='api'),# 扫描后通过这个api 获得AR模型配置
    url(r'^test$', test, name='test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # 设置访问静态文件



