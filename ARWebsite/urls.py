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
    url(r'^$', home, name='home'),  # 首页
    url(r'^index.html$', index, name='index'),  # 管理首页
    url(r'^register.html$', do_register, name='register'),  # 注册页面
    url(r'^login.html$', do_login, name='login'),  # 登陆页面
    url(r'^logout.html$', do_logout, name='logout'),  # 注销
    url(r'^add-model.html$', add_model, name='add_mode'),  # 增加AR模型页面
    url(r'^delete.html$', delete_model, name='delete_mode'),  # 删除模型
    url(r'^models.html$', models, name='model'),  # AR模型列表页面
    url(r'^my-account.html$', my_account, name='my_account'),  # 账户信息页面
    url(r'^edit-profile.html$', edit_profile, name='edit_profile'),  # 账户管理页面
    url(r'^download.html', download, name='download'),  # 下载页面
    url(r'^help.html$', help_page, name='help_page'),  # 帮助页面
    url(r'^view-model.html$', view_model, name='view_model'),  # 查看AR模型详细信息页面
    url(r'^arConfigInfo-api$', ar_config_info_api, name='api'),  # 扫描后通过这个api 获得AR模型配置
    url(r'^arComment-api$', ar_comment_api, name='comment_api'),  # 用于提交评论
    url(r'^arComment-get-api$', get_ar_comment_api, name='comment_get_api'),  # 用于获取评论
    url(r'^product-link-clicked-api$', product_link_clicked_api, name='product_link_clicked_api'),  # 传递商品链接被点击的消息
    url(r'^arLike-api$', ar_like_api, name='like_api'),  # 用于点赞
    url(r'^arLike-get-api$', get_ar_like_api, name='like_get_api'),  # 用于获取点赞数
    url(r'^404.html', page404, name='404'),  # 404
    url(r'^api-test', api_test, name='api_test'),  # 用于产生测试数据
    url(r'^admin/server$', server, name='server'),   # 服务器负载查看
    url(r'^admin/server-info-api$', server_info_api, name='server_info_api'),  # 服务器负载信息api

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 设置访问静态文件
